from django.urls import path
from .views import analyze_tasks, suggest_tasks  # ✅ correct import

urlpatterns = [
    path('api/tasks/analyze/', analyze_tasks),
    path('api/tasks/suggest/', suggest_tasks),
]
