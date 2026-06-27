import json
import os
import re
from collections import Counter

from flask import Flask, jsonify, render_template, request


QUALITY_REPORT_FILE = "generated_tasks_quality_report.json"
VERIFIED_DATASET_FILE = "distilled_dataset/verified_tasks.json"
AGENTGEN_DATASET_FILE = "AgentGen-main/src/results/it12/merged_gpt_it12.json"
STUDENT_MODEL_FILE = "distilled_model/student_quality_model.json"
STUDENT_TRAINING_FILE = "distilled_model/student_training_summary.json"
STUDENT_EVALUATION_FILE = "distilled_model/student_evaluation.json"
STUDENT_PREDICTIONS_FILE = "distilled_model/student_predictions.json"

app = Flask(__name__)

_multi_retriever = None
_rag_error = None


DOMAIN_ALIASES = {
    "study": [
        "study",
        "exam",
        "quiz",
        "notes",
        "chapter",
        "learn"
    ],
    "event": [
        "event",
        "venue",
        "catering",
        "speaker",
        "guests",
        "workshop"
    ],
    "travel": [
        "travel",
        "trip",
        "pack",
        "packing",
        "flight",
        "hotel",
        "passport",
        "bags",
        "vacation"
    ],
    "cooking": [
        "cook",
        "cooking",
        "meal",
        "dinner",
        "ingredients",
        "vegetables"
    ],
    "project": [
        "project",
        "prototype",
        "requirements",
        "design",
        "tests",
        "deliver"
    ],
    "shopping": [
        "shopping",
        "shop",
        "store",
        "buy",
        "payment",
        "list"
    ]
}

ACTION_LABELS = {
    "prepare-passport": "Check passport, visa, IDs, and travel documents.",
    "book-flight": "Book transportation and keep confirmation details handy.",
    "book-hotel": "Confirm accommodation, address, check-in time, and backup contact.",
    "pack-bags": "Pack clothes, toiletries, chargers, medicine, documents, and destination-specific items.",
    "start-trip": "Do a final home check, leave on time, and start the trip.",
    "study-chapter1": "Study the first topic and write short notes.",
    "study-chapter2": "Study the next topic after the basics are clear.",
    "review-notes": "Review notes and mark weak points.",
    "take-quiz": "Take a quiz to test understanding.",
    "take-mock-exam": "Simulate the final exam conditions.",
    "pass-exam": "Complete the final exam goal.",
    "book-venue": "Book the venue and confirm availability.",
    "arrange-catering": "Arrange catering after the venue is confirmed.",
    "confirm-speaker": "Confirm the speaker and agenda.",
    "invite-guests": "Invite guests and track responses.",
    "prepare-event": "Finalize the event checklist.",
    "prepare-ingredients": "Prepare all ingredients.",
    "chop-vegetables": "Chop vegetables and prep cooking tools.",
    "cook-sauce": "Cook the main sauce or base.",
    "plate-meal": "Plate the meal.",
    "serve-dinner": "Serve dinner.",
    "write-requirements": "Write the requirements.",
    "approve-design": "Approve the design.",
    "build-prototype": "Build the prototype.",
    "run-tests": "Run tests and fix failures.",
    "deliver-project": "Deliver the project.",
    "make-list": "Make the shopping list.",
    "visit-store": "Visit the store.",
    "buy-items": "Buy the needed items.",
    "complete-payment": "Complete payment.",
    "finish-shopping": "Finish the shopping task."
}


def load_json(path, default):
    if not os.path.exists(path):
        return default

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def read_text(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def get_quality_report():
    return load_json(
        QUALITY_REPORT_FILE,
        {
            "total_tasks": 0,
            "accepted_count": 0,
            "rejected_count": 0,
            "threshold": 80,
            "results": []
        }
    )


def get_verified_dataset():
    return load_json(
        VERIFIED_DATASET_FILE,
        []
    )


def get_model_phase():
    return {
        "training": load_json(
            STUDENT_TRAINING_FILE,
            {}
        ),
        "evaluation": load_json(
            STUDENT_EVALUATION_FILE,
            {}
        ),
        "predictions": load_json(
            STUDENT_PREDICTIONS_FILE,
            []
        )
    }


class KeywordRetriever:
    def __init__(self, dataset):
        self.dataset = dataset

    def retrieve(self, query, top_k=5):
        query_terms = set(tokenize(query))
        detected_domain = detect_domain(query)
        scored = []

        for sample in self.dataset:
            text = sample.get(
                "environment_text",
                ""
            )
            terms = set(tokenize(text))
            overlap = len(query_terms.intersection(terms))
            sample_id = sample.get(
                "id",
                ""
            ).lower()

            if (
                detected_domain
                and detected_domain in sample_id
            ):
                overlap += 12
            if sample.get("source") == "verified_tasks":
                overlap += 2

            scored.append(
                (
                    overlap,
                    sample
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            sample
            for score, sample in scored[:top_k]
            if score > 0
        ]


def normalize_agentgen_sample(sample, index):
    if "environment_text" in sample:
        return sample

    conversations = sample.get(
        "conversations",
        []
    )
    first_message = (
        conversations[0].get(
            "value",
            ""
        )
        if conversations
        else json.dumps(
            sample,
            ensure_ascii=False
        )[:1200]
    )

    return {
        "id": sample.get(
            "id",
            f"agentgen-{index + 1}"
        ),
        "environment_text": first_message,
        "source": "AgentGen"
    }


def load_agentgen_samples():
    raw_dataset = load_json(
        AGENTGEN_DATASET_FILE,
        []
    )

    return [
        normalize_agentgen_sample(
            sample,
            index
        )
        for index, sample in enumerate(raw_dataset)
    ]


def get_retriever():
    global _multi_retriever
    global _rag_error

    if _multi_retriever is not None:
        return _multi_retriever

    verified_samples = [
        {
            "id": record["id"],
            "environment_text": (
                record.get("id", "")
                + "\n"
                + record.get("domain_pddl", "")
                + "\n"
                + record.get("problem_pddl", "")
            ),
            "source": "verified_tasks"
        }
        for record in get_verified_dataset()
    ]

    dataset = (
        verified_samples
        + load_agentgen_samples()
    )

    if not dataset:
        dataset = verified_samples

    use_embedding_rag = (
        os.getenv("ENABLE_EMBEDDING_RAG", "0") == "1"
    )

    if not use_embedding_rag:
        from rag.multi_query_retriever import MultiQueryRetriever

        _rag_error = (
            "Fast demo mode is using multi-query keyword retrieval. "
            "Set ENABLE_EMBEDDING_RAG=1 to use sentence-transformer embeddings."
        )
        _multi_retriever = MultiQueryRetriever(
            KeywordRetriever(dataset)
        )
        return _multi_retriever

    try:
        from rag.embedding_retriever import EmbeddingRetriever
        from rag.multi_query_retriever import MultiQueryRetriever

        embedding_retriever = EmbeddingRetriever(
            dataset
        )
        _multi_retriever = MultiQueryRetriever(
            embedding_retriever
        )
        _rag_error = None
    except Exception as exc:
        from rag.multi_query_retriever import MultiQueryRetriever

        _rag_error = str(exc)
        _multi_retriever = MultiQueryRetriever(
            KeywordRetriever(dataset)
        )

    return _multi_retriever


def tokenize(text):
    return re.findall(
        r"[a-zA-Z][a-zA-Z0-9_-]*",
        text.lower()
    )


def score_class(score):
    if score >= 90:
        return "score-high"

    if score >= 80:
        return "score-medium"

    return "score-low"


def detect_domain(user_input):
    tokens = set(tokenize(user_input))
    best_domain = None
    best_score = 0

    for domain, aliases in DOMAIN_ALIASES.items():
        score = len(
            tokens.intersection(
                set(aliases)
            )
        )
        if score > best_score:
            best_domain = domain
            best_score = score

    return best_domain


def is_user_planning_request(user_input):
    tokens = set(tokenize(user_input))
    planning_words = {
        "plan",
        "planning",
        "help",
        "organize",
        "schedule",
        "checklist",
        "steps",
        "todo",
        "prepare",
        "pack"
    }

    return bool(
        tokens.intersection(planning_words)
    )


def wants_research_summary(user_input):
    tokens = set(tokenize(user_input))

    return bool(
        tokens.intersection(
            {
                "thesis",
                "comparison",
                "compare",
                "original",
                "agentgen",
                "baseline",
                "results",
                "experiment",
                "evaluation"
            }
        )
    )


def find_relevant_verified_records(user_input, limit=4):
    records = get_verified_dataset()
    query_terms = set(tokenize(user_input))
    lowered_input = user_input.lower()
    detected_domain = detect_domain(user_input)
    scored = []

    for record in records:
        record_id = record.get(
            "id",
            ""
        ).lower()
        text = (
            record.get("id", "")
            + " "
            + record.get("domain_pddl", "")
            + " "
            + record.get("problem_pddl", "")
        )
        overlap = len(
            query_terms.intersection(
                set(tokenize(text))
            )
        )

        if record_id in lowered_input:
            overlap += 5
        for domain_hint in [
            "study",
            "event",
            "travel",
            "cooking",
            "project",
            "shopping"
        ]:
            if (
                domain_hint in lowered_input
                and domain_hint in record_id
            ):
                overlap += 8
        if (
            detected_domain
            and detected_domain in record_id
        ):
            overlap += 14
        if (
            "hard" in lowered_input
            and "chain_goal_5" in record_id
        ):
            overlap += 4
        if (
            "hard" in lowered_input
            and "chain_goal_6" in record_id
        ):
            overlap += 4
        if (
            "medium" in lowered_input
            and (
                "chain_goal_3" in record_id
                or "chain_goal_4" in record_id
            )
        ):
            overlap += 4
        if (
            "easy" in lowered_input
            and "chain_goal_1" in record_id
        ):
            overlap += 4
        if (
            detected_domain
            and "chain_goal_5" in record_id
        ):
            overlap += 3

        scored.append(
            (
                overlap,
                record
            )
        )

    scored.sort(
        key=lambda item: (
            item[0],
            item[1].get(
                "quality_score",
                0
            )
        ),
        reverse=True
    )

    return [
        record
        for score, record in scored[:limit]
        if score > 0
    ] or records[:limit]


def extract_action_sequence(domain_pddl):
    action_names = re.findall(
        r"\(:action\s+([a-zA-Z0-9_-]+)",
        domain_pddl
    )

    return [
        action
        for action in action_names
        if "unused" not in action
    ]


def build_user_plan(user_input, best_record):
    if not best_record:
        return None

    domain = detect_domain(user_input)
    actions = extract_action_sequence(
        best_record.get(
            "domain_pddl",
            ""
        )
    )

    if not actions:
        return None

    checklist = [
        ACTION_LABELS.get(
            action,
            action.replace(
                "-",
                " "
            ).capitalize()
        )
        for action in actions
    ]

    title = (
        "Trip packing plan"
        if domain == "travel"
        else "Action plan"
    )

    return {
        "domain": domain or "planning",
        "title": title,
        "actions": actions,
        "checklist": checklist,
        "source_task": best_record["id"],
        "quality_score": best_record["quality_score"],
        "decision": best_record["decision"]
    }


def predict_with_student_model(text):
    model = load_json(
        STUDENT_MODEL_FILE,
        None
    )

    if not model:
        return None

    from distillation.student_quality_model import predict

    return predict(
        model,
        text
    )


def summarize_failures(records):
    failures = Counter()

    for record in records:
        summary = record.get(
            "verifier_summary",
            {}
        )
        if not summary.get(
            "reachable",
            True
        ):
            failures["unreachable_goal"] += 1
        if summary.get(
            "trivial_problem",
            False
        ):
            failures["trivial_goal"] += 1
        if not summary.get(
            "object_consistency",
            True
        ):
            failures["object_consistency"] += 1
        if summary.get(
            "dead_action_count",
            0
        ):
            failures["dead_actions"] += 1

    return dict(failures)


def build_chat_response(user_input):
    if not user_input.strip():
        return {
            "reply": "Send me a planning request, a domain name, or PDDL text and I will plan, retrieve context, run the quality model, and explain the result.",
            "steps": []
        }

    retriever = get_retriever()
    queries = retriever.generate_queries(
        user_input
    )
    rag_results = retriever.retrieve(
        user_input,
        top_k=4
    )
    verified_records = find_relevant_verified_records(
        user_input
    )

    model_input = user_input
    if verified_records:
        model_input = (
            verified_records[0].get("domain_pddl", "")
            + "\n"
            + verified_records[0].get("problem_pddl", "")
        )

    prediction = predict_with_student_model(
        model_input
    )
    report = get_quality_report()
    model_phase = get_model_phase()
    include_research_summary = wants_research_summary(
        user_input
    )
    best_record = (
        verified_records[0]
        if verified_records
        else None
    )
    user_plan = (
        build_user_plan(
            user_input,
            best_record
        )
        if is_user_planning_request(user_input)
        else None
    )
    failure_summary = summarize_failures(
        [best_record]
        if (
            user_plan
            and best_record
        )
        else verified_records
    )
    model_decision = (
        prediction["decision"]
        if prediction
        else "unavailable"
    )
    estimated_score = (
        prediction["estimated_quality_score"]
        if prediction
        else "n/a"
    )

    if user_plan:
        checklist_text = "\n".join(
            f"{index + 1}. {item}"
            for index, item in enumerate(
                user_plan["checklist"]
            )
        )
        reply_parts = [
            (
                f"Here is a practical {user_plan['title'].lower()} "
                "generated from the closest verified planning chain:\n\n"
                f"{checklist_text}"
            ),
            (
                "\nI also checked the plan through the project pipeline: "
                "multi-query retrieval, verified PDDL task matching, and "
                "the distilled student quality model."
            )
        ]
    else:
        reply_parts = [
            (
                "I treated your input as a planning-task quality question and ran "
                "the project pipeline over it: multi-query retrieval, verified "
                "task lookup, and the distilled student quality model."
            )
        ]

    if best_record:
        reply_parts.append(
            "The closest verified task is "
            f"{best_record['id']} with verifier decision "
            f"{best_record['decision']} and score "
            f"{best_record['quality_score']}/100."
        )

    if prediction:
        reply_parts.append(
            "The student model predicts "
            f"{model_decision} with an estimated quality score of "
            f"{estimated_score}/100 for the retrieved context."
        )

    if failure_summary:
        reply_parts.append(
            "The main verifier signals in the matched examples are: "
            + ", ".join(
                f"{name.replace('_', ' ')}={count}"
                for name, count in failure_summary.items()
            )
            + "."
        )

    if include_research_summary:
        reply_parts.append(
            "For the thesis comparison, the current benchmark contains "
            f"{report['total_tasks']} verified tasks, "
            f"{report['accepted_count']} accepted and "
            f"{report['rejected_count']} rejected. "
            "This gives a clearer comparison than the earlier three-task demo, "
            "but you should report it as a controlled benchmark unless you later "
            "run the full AgentGen generation loop."
        )
    elif user_plan:
        reply_parts.append(
            "Tell me your destination, trip length, weather, and whether this is business or vacation, and I can refine the packing list."
        )

    steps = [
        {
            "title": "Input received",
            "detail": user_input
        },
        {
            "title": "Multi-query RAG",
            "detail": "Generated queries: " + "; ".join(queries),
            "items": [
                result.get(
                    "id",
                    "retrieved-sample"
                )
                for result in rag_results
            ],
            "warning": (
                f"Embedding RAG fell back to keyword retrieval: {_rag_error}"
                if _rag_error
                else None
            )
        },
        {
            "title": "Verifier memory",
            "detail": (
                f"Matched {len(verified_records)} verified PDDL tasks "
                "from the quality report."
            ),
            "items": [
                (
                    f"{record['id']}: {record['decision']} "
                    f"({record['quality_score']}/100)"
                )
                for record in verified_records
            ]
        },
        {
            "title": "Planning tool",
            "detail": (
                (
                    f"Generated a {user_plan['domain']} action plan from "
                    f"{user_plan['source_task']}."
                )
                if user_plan
                else "No direct user task plan was requested; stayed in verifier analysis mode."
            ),
            "items": (
                user_plan["checklist"]
                if user_plan
                else []
            )
        },
        {
            "title": "Student model",
            "detail": (
                f"Prediction: {model_decision}; "
                f"estimated score: {estimated_score}; "
                f"training examples: "
                f"{model_phase['training'].get('training_examples', 0)}"
            )
        },
        {
            "title": "Response composed",
            "detail": (
                "Combined retrieval context, verifier diagnostics, model prediction, and an actionable plan."
                if user_plan
                else "Combined retrieval context, verifier diagnostics, model prediction, and benchmark summary."
            )
        }
    ]

    return {
        "reply": " ".join(reply_parts),
        "steps": steps,
        "model_prediction": prediction,
        "plan": user_plan,
        "matched_records": [
            {
                "id": record["id"],
                "decision": record["decision"],
                "quality_score": record["quality_score"],
                "summary": record.get(
                    "verifier_summary",
                    {}
                )
            }
            for record in verified_records
        ],
        "rag_results": [
            {
                "id": result.get(
                    "id",
                    "retrieved-sample"
                ),
                "preview": result.get(
                    "environment_text",
                    ""
                )[:260]
            }
            for result in rag_results
        ]
    }


@app.route("/")
def home():
    report = get_quality_report()
    verified_dataset = get_verified_dataset()
    model_phase = get_model_phase()

    return render_template(
        "index.html",
        report=report,
        verified_dataset=verified_dataset,
        model_phase=model_phase,
        score_class=score_class
    )


@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():
    payload = request.get_json(
        silent=True
    ) or {}
    user_input = payload.get(
        "message",
        ""
    )

    try:
        result = build_chat_response(
            user_input
        )
        return jsonify(result)
    except Exception as exc:
        return jsonify({
            "reply": (
                "I could not complete the full agentic pipeline. "
                f"Error: {exc}"
            ),
            "steps": [
                {
                    "title": "Pipeline error",
                    "detail": str(exc)
                }
            ]
        }), 500


@app.route(
    "/search",
    methods=["GET", "POST"]
)
def search():
    results = []
    query = ""
    error = None

    if request.method == "POST":
        query = request.form["query"]

        try:
            retriever = get_retriever()
            results = retriever.retrieve(
                query
            )
        except Exception as exc:
            error = str(exc)

    return render_template(
        "results.html",
        results=results,
        query=query,
        error=error
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )
