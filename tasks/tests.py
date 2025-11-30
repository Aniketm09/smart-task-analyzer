# tasks/tests.py
from django.test import TestCase
from datetime import date, timedelta
from .scoring import score_task
from .utils import detect_cycle

class ScoringAndCycleTests(TestCase):
    def test_overdue_has_higher_score_than_future(self):
        today = date.today()
        overdue = {"id":"a","importance":5,"estimated_hours":2,"due_date": today - timedelta(days=1), "dependencies":[]}
        future = {"id":"b","importance":5,"estimated_hours":2,"due_date": today + timedelta(days=10), "dependencies":[]}
        so = score_task(overdue, today)
        sf = score_task(future, today)
        self.assertTrue(so > sf, f"overdue {so} should be > future {sf}")

    def test_quick_win_boost(self):
        today = date.today()
        short = {"id":"s","importance":5,"estimated_hours":1,"due_date": today + timedelta(days=5), "dependencies":[]}
        long =  {"id":"l","importance":5,"estimated_hours":8,"due_date": today + timedelta(days=5), "dependencies":[]}
        ss = score_task(short, today)
        sl = score_task(long, today)
        self.assertTrue(ss > sl, f"short {ss} should be > long {sl}")

    def test_detect_cycle_true(self):
        tasks = [
            {"id":"a", "dependencies":["b"]},
            {"id":"b", "dependencies":["a"]}
        ]
        self.assertTrue(detect_cycle(tasks))

    def test_detect_cycle_false(self):
        tasks = [
            {"id":"a", "dependencies":[]},
            {"id":"b", "dependencies":["a"]}
        ]
        self.assertFalse(detect_cycle(tasks))
