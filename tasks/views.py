from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from .utils import detect_cycle
from .scoring import score_task
from .models import Task
import datetime


@api_view(['POST'])
def analyze_tasks(request):
    tasks = request.data

    if not isinstance(tasks, list):
        return Response({"error": "Input must be a list"}, status=400)

    # Circular dependency check
    if detect_cycle(tasks):
        return Response({"error": "Circular dependency detected!"}, status=400)

    today = date.today()

    # convert & score
    for t in tasks:
        due = t.get("due_date")
        if due:
            try:
                t["due_date"] = datetime.date.fromisoformat(due)
            except:
                t["due_date"] = None
        else:
            t["due_date"] = None

        t["score"] = score_task(t, today)

    tasks.sort(key=lambda x: x["score"], reverse=True)
    return Response(tasks)


@api_view(['GET'])
def suggest_tasks(request):
    db_tasks = list(Task.objects.all().values())

    if not db_tasks:
        return Response({"error": "No tasks in database"}, status=400)

    today = date.today()
    result = []

    for t in db_tasks:
        task = {
            "id": t["id"],
            "title": t["title"],
            "importance": t["importance"],
            "estimated_hours": t["estimated_hours"],
            "due_date": t["due_date"],
            "dependencies": t["dependencies"]
        }
        task["score"] = score_task(task, today)

        reason = []
        if task["due_date"] and (task["due_date"] - today).days < 0:
            reason.append("Overdue")
        if task["importance"] >= 8:
            reason.append("High Importance")
        if task["estimated_hours"] and task["estimated_hours"] <= 2:
            reason.append("Quick Win")
        if task["dependencies"]:
            reason.append("Blocks Other Tasks")

        result.append({
            "task": task,
            "reason": " | ".join(reason) if reason else "Balanced"
        })

    result.sort(key=lambda x: x["task"]["score"], reverse=True)
    return Response(result[:3])
