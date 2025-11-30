import datetime

def score_task(task, today):
    score = 0

    score += task["importance"] * 2

    if task["due_date"]:
        days = (task["due_date"] - today).days
        if days < 0:
            score += 12
        else:
            score += max(0, 10 - days)

    e = task.get("estimated_hours")
    if e:
        if e <= 2:
            score += 6
        elif e <= 5:
            score += 3
        else:
            score -= 1
    else:
        score -= 3

    if task["dependencies"]:
        score += 4

    return score
