def verify_plan(plan_text, total_domain_actions=6):

    actions = []

    for line in plan_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("INFO"):
            continue

        actions.append(line)

    action_count = len(actions)

    # --------------------
    # Difficulty
    # --------------------

    if action_count <= 2:
        difficulty = "Easy"
        difficulty_score = 30

    elif action_count <= 5:
        difficulty = "Medium"
        difficulty_score = 60

    else:
        difficulty = "Hard"
        difficulty_score = 90

    # --------------------
    # Coverage
    # --------------------

    coverage = round(
        (action_count / total_domain_actions) * 100,
        2
    )

    if coverage > 100:
        coverage = 100

    # --------------------
    # Redundancy
    # --------------------

    unique_actions = set(actions)

    redundancy_score = round(
        (len(unique_actions) / max(action_count, 1)) * 100,
        2
    )

    # --------------------
    # Reachability
    # --------------------

    goal_reachable = action_count > 0

    # --------------------
    # Final Quality Score
    # --------------------

    quality_score = round(
        (
            coverage +
            redundancy_score +
            difficulty_score
        ) / 3,
        2
    )

    return {
        "goal_reachable": goal_reachable,
        "difficulty": difficulty,
        "difficulty_score": difficulty_score,
        "action_count": action_count,
        "coverage": coverage,
        "redundancy_score": redundancy_score,
        "quality_score": quality_score
    }