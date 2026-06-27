import json
import math
import os
import re
from collections import Counter, defaultdict


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]*")


def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(path, data):
    directory = os.path.dirname(path)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def tokenize(text):
    return [
        token.lower()
        for token in TOKEN_RE.findall(text)
    ]


def record_text(record):
    return (
        record.get("domain_pddl", "")
        + "\n"
        + record.get("problem_pddl", "")
    )


def train_model(records):
    label_counts = Counter()
    token_counts = defaultdict(Counter)
    total_tokens = Counter()
    score_totals = Counter()

    vocabulary = set()

    for record in records:
        label = record["decision"]
        tokens = tokenize(
            record_text(record)
        )

        label_counts[label] += 1
        score_totals[label] += record.get(
            "quality_score",
            0
        )

        for token in tokens:
            token_counts[label][token] += 1
            total_tokens[label] += 1
            vocabulary.add(token)

    labels = sorted(label_counts)

    if not labels:
        raise ValueError(
            "Cannot train student model with no records."
        )

    average_scores = {
        label: (
            score_totals[label]
            / label_counts[label]
        )
        for label in labels
    }

    return {
        "model_type": "multinomial_naive_bayes",
        "labels": labels,
        "label_counts": dict(label_counts),
        "token_counts": {
            label: dict(counts)
            for label, counts in token_counts.items()
        },
        "total_tokens": dict(total_tokens),
        "vocabulary": sorted(vocabulary),
        "average_scores": average_scores
    }


def predict(model, text):
    tokens = tokenize(text)
    token_counter = Counter(tokens)
    labels = model["labels"]
    vocabulary = model["vocabulary"]
    vocabulary_size = max(
        len(vocabulary),
        1
    )
    total_records = sum(
        model["label_counts"].values()
    )

    scores = {}

    for label in labels:
        label_count = model["label_counts"][label]
        prior = math.log(
            label_count / total_records
        )
        label_token_counts = model["token_counts"].get(
            label,
            {}
        )
        total_label_tokens = model["total_tokens"].get(
            label,
            0
        )
        denominator = (
            total_label_tokens
            + vocabulary_size
        )

        score = prior

        for token, count in token_counter.items():
            token_count = label_token_counts.get(
                token,
                0
            )
            likelihood = (
                token_count + 1
            ) / denominator

            score += (
                math.log(likelihood)
                * count
            )

        scores[label] = score

    predicted_label = max(
        scores,
        key=scores.get
    )

    expected_score = round(
        model["average_scores"].get(
            predicted_label,
            0
        ),
        2
    )

    return {
        "decision": predicted_label,
        "estimated_quality_score": expected_score,
        "label_scores": scores
    }


def evaluate_records(records):
    predictions = []

    if len(records) == 1:
        model = train_model(records)
        prediction = predict(
            model,
            record_text(records[0])
        )
        predictions.append({
            "id": records[0]["id"],
            "actual_decision": records[0]["decision"],
            "predicted_decision": prediction["decision"],
            "actual_quality_score": records[0]["quality_score"],
            "estimated_quality_score": prediction["estimated_quality_score"],
            "correct": prediction["decision"] == records[0]["decision"]
        })
    else:
        for index, record in enumerate(records):
            train_records = (
                records[:index]
                + records[index + 1:]
            )
            model = train_model(train_records)
            prediction = predict(
                model,
                record_text(record)
            )

            predictions.append({
                "id": record["id"],
                "actual_decision": record["decision"],
                "predicted_decision": prediction["decision"],
                "actual_quality_score": record["quality_score"],
                "estimated_quality_score": prediction["estimated_quality_score"],
                "correct": prediction["decision"] == record["decision"]
            })

    correct = sum(
        1
        for item in predictions
        if item["correct"]
    )

    total = len(predictions)

    return {
        "evaluation_method": "leave_one_out",
        "total_examples": total,
        "correct": correct,
        "accuracy": (
            round(correct / total, 4)
            if total
            else 0
        ),
        "predictions": predictions
    }
