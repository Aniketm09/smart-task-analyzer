from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from .models import Task
from .utils import detect_cycle
from .scoring import score_task  
import datetime

@api_view(['POST'])
def analyze_tasks(request):
    tasks = request.data

    if not isinstance(tasks, list):
        return Response({"error": "Input should be a list of tasks"}, status=400)

    today = date.today()
    for t in tasks:
      
        due = t.get("due_date")
        if due:
            try:
                t["due_date"] = datetime.date.fromisoformat(due)
            except:
                t["due_date"] = None
        else:
            t["due_date"] = None

        imp = t.get("importance")
        if not (isinstance(imp, int) and 1 <= imp <= 10):
            t["importance"] = 5  

   
    if detect_cycle(tasks):
        return Response({"error": "Circular dependency detected!"}, status=400)

    for t in tasks:
        t["score"] = score_task(t, today)

    tasks.sort(key=lambda x: x["score"], reverse=True)
    return Response(tasks)


@api_view(['GET'])
def suggest_tasks(request):
    
    db_tasks = list(Task.objects.all().values())

    if not db_tasks:
        return Response({"error": "No tasks in database"}, status=400)

    today = date.today()
    scored = []

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
    
        why = []
        if task["due_date"] and (task["due_date"] - today).days < 0:
            why.append("This task is past-due")
        if task["importance"] >= 8:
            why.append("User marked it very important")
        if task["estimated_hours"] and task["estimated_hours"] <= 2:
            why.append("Small effort → quick completion")
        if task["dependencies"]:
            why.append("It unlocks dependent work")

        scored.append({
            "task": task,
            "reason": " | ".join(why) if why else "Balanced score among factors"
        })

    scored.sort(key=lambda x: x["task"]["score"], reverse=True)
    return Response({"today_top3": scored[:3]})
