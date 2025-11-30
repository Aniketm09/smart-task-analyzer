import datetime
from collections import defaultdict

def detect_cycle(task_list):
    graph = defaultdict(list)
    for task in task_list:
        tid = task.get("id")
        for dep in task.get("dependencies", []):
            graph[tid].append(dep)

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for nei in graph[node]:
            if dfs(nei):
                return True
        stack.remove(node)
        return False

    for n in graph:
        if dfs(n):
            return True
    return False


def score_task(task, today):
    score = 0

    # Importance
    imp = task.get("importance")
    if isinstance(imp, int) and 1 <= imp <= 10:
        score += imp * 2
    else:
        score += 5

    # Urgency
    due = task.get("due_date")
    if isinstance(due, datetime.date):
        days = (due - today).days
        if days < 0:
            score += 12
        else:
            score += max(0, 10 - days)
    else:
        score += 4

    # Effort (Quick win)
    hrs = task.get("estimated_hours")
    if isinstance(hrs, (int,float)):
        if hrs <= 2:
            score += 6
        elif hrs <= 5:
            score += 3
        else:
            score -= 1
    else:
        score -= 3

    # Blocking dependencies bonus
    if task.get("dependencies"):
        score += 4

    return score
