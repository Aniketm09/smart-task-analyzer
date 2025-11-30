from django.test import TestCase
from datetime import date, timedelta
from .utils import detect_cycle, score_task

class AlgorithmTests(TestCase):

    def test_overdue_task_scores_high(self):
        t = {"importance":9, "due_date": date.today() - timedelta(days=2), "dependencies":[]}
        s = score_task(t, date.today())
        self.assertTrue(s > 20)

    def test_quick_win_bonus(self):
        t = {"importance":5, "estimated_hours":1.5, "due_date": date.today() + timedelta(days=5), "dependencies":[]}
        s = score_task(t, date.today())
        self.assertTrue(s >= 15)

    def test_cycle_detect(self):
        tasks = [
            {"id":"a","dependencies":["b"]},
            {"id":"b","dependencies":["a"]}
        ]
        self.assertTrue(detect_cycle(tasks))

    def test_no_cycle(self):
        tasks = [
            {"id":"a","dependencies":["b"]},
            {"id":"b","dependencies":[]}
        ]
        self.assertFalse(detect_cycle(tasks))
