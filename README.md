# Smart Task Analyzer

A small API-first task scoring system that ranks tasks using logical priority instead of simple sorting.

## 1. Design Decisions

- Priority is **not stored**—it is **computed dynamically** using `tasks/scoring.py`.
- The goal is to help users decide **what to work on next**, not build a full planner.
- Logic is deterministic, minimal, and easy to audit for assessment.

---

## 2. Priority Algorithm (My Logic)

| Factor              | Logic Used                                                        |
| ------------------- | ----------------------------------------------------------------- |
| Importance          | importance × 2 (defaults to 5 if missing)                         |
| Due Date / Urgency  | Closer dates → higher score; overdue tasks get +12 urgency boost  |
| Effort              | ≤ 2 hours → +6 “quick win” bonus; larger tasks get a mild penalty |
| Dependencies        | Tasks unlocking other tasks get +4                                |
| Missing Data        | Invalid/missing fields lower score slightly (no crashes)          |
| Circular Dependency | Detected using DFS in `tasks/utils.py`                            |

Final score = combination of all factors → **sorted high → low**.

---

## 3. Edge Case Handling

- **Overdue tasks** are boosted to ensure visibility.
- **Null or invalid due dates** treated as medium urgency.
- **Out-of-range importance** resets to default 5.
- **Circular dependencies** trigger an API error instead of infinite recursion.
- Minimal config to keep logic predictable and clean.

---

## 4. API Endpoints

| Method | Endpoint              | Purpose                                                |
| ------ | --------------------- | ------------------------------------------------------ |
| POST   | `/api/tasks/analyze/` | Scores & returns sorted tasks including priority score |
| GET    | `/api/tasks/suggest/` | Returns top 3 tasks with short reasoning               |

---

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

---

## 6. Frontend Overview

The frontend is simple (HTML/CSS/JS) and includes:

- **Task Form** for adding single tasks
- **Bulk JSON Input** for fast testing
- **Analyze Button** to call the backend
- **Color-coded priority list** (High/Medium/Low)
- **Strategy Selector**: Fastest Wins, High Impact, Deadline Driven, Smart Balance
- Fully responsive & minimal by design

---

## 7. Tests Included

Located in `tasks/tests.py`:

- Urgency scoring test
- Effort scoring test
- Circular dependency detection test

Run tests:

```bash
python manage.py test

## 8. Time Breakdown

| Task                    | Duration   |
| ----------------------- | ---------- |
| Algorithm design        | ~45 min    |
| Backend (models, views) | ~1 hr      |
| API testing             | ~20 min    |
| Frontend (UI + JS)      | ~1 hr      |
| Tests                   | ~20 min    |
| Documentation           | ~15–20 min |

**Total: ~3.5–4 hours**

## 9. Bonus Work

| Feature                       | Status         |
| ----------------------------- | -------------- |
| Circular dependency detection | ✔ Done         |
| Multiple sorting strategies   | ✔ Done         |

## 10. Future Improvements

* Add user-controlled scoring weights
* Better UI/UX (drag-and-drop + charts)
* Dependency graph visualization
* Persistent task storage
* Smart learning system for better future suggestions


## 11. Final Notes

This project focuses on clean thinking, a logical scoring model, clear code separation, and a lightweight functional UI.
The system remains small, predictable, and simple for evaluation while covering all core assessment requirements.


```
