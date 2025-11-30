# Smart Task Analyzer

A small API-first task scoring system that ranks tasks using logical priority instead of simple sorting.

## 1. Design Decisions

- The system does **not store priority manually**, it **calculates it dynamically** using a scoring formula written in `tasks/scoring.py`.
- The algorithm focuses on **helping a user pick next work**, not building a full task planner.

## 2. Priority Algorithm (My Logic)

The `score_task()` function was designed with this simple approach:

| Factor              | Logic Used                                                           |
| ------------------- | -------------------------------------------------------------------- |
| Importance          | importance × 2, default 5 if missing                                 |
| Due Date / Urgency  | Closer dates increase score; overdue tasks get +12 boost             |
| Effort              | Tasks ≤ 2 hours get +6 quick-win bonus; long tasks get small penalty |
| Dependencies        | Tasks that unblock other work get +4 bonus                           |
| Missing Data        | Invalid values reduce score slightly but do not crash the API        |
| Circular Dependency | Detected before scoring using DFS logic in `tasks/utils.py`          |

Final score = combination of all, then tasks are sorted **high → low** score.

## 3. How Edge Cases Are Handled

- **Overdue tasks** are not ignored, they are intentionally boosted to ensure visibility.
- **Invalid or null due dates** are accepted but treated as moderate urgency.
- **Importance outside 1–10** is replaced with default 5.
- **Circular dependency** returns API error instead of infinite loop or crash.
- The algorithm is **not user-configurable** currently to keep logic minimal and deterministic for assessment.

## 4. API Endpoints

| Method | Endpoint              | Purpose                                                |
| ------ | --------------------- | ------------------------------------------------------ |
| POST   | `/api/tasks/analyze/` | Scores & returns sorted tasks including priority score |
| GET    | `/api/tasks/suggest/` | Returns top 3 ranked DB tasks with short reason blocks |

## 5. Setup to Run Locally

```bash
git clone <repo>
cd Smart Task Analyzer
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
