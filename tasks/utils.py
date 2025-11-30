import datetime
from collections import defaultdict

def detect_cycle(tasks):
   
    graph = {}
    for t in tasks:
        tid = str(t["id"])
        graph[tid] = []

    for t in tasks:
        tid = str(t["id"])
        for dep in (t.get("dependencies") or []):
            dep = str(dep)
            if dep in graph:      
                graph[dep].append(tid)

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True  

        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True

        stack.remove(node)
        return False
    
    for node in list(graph.keys()):
        if dfs(node):
            return True

    return False


def score_task(task, today):
    score = 0

    imp = task.get("importance")
    if isinstance(imp, int) and 1 <= imp <= 10:
        score += imp * 2
    else:
        score += 5

    due = task.get("due_date")
    if isinstance(due, datetime.date):
        days = (due - today).days
        if days < 0:
            score += 12
        else:
            score += max(0, 10 - days)
    else:
        score += 4

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

    if task.get("dependencies"):
        score += 4

    return score
