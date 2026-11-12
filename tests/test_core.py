import unittest,copy,json
from planned_event_tense_ledger import run
DEMO={'now': '2026-11-12T12:00:00Z', 'events': [{'id': 'meeting', 'kind': 'planned', 'target_at': '2026-11-13T10:00:00Z', 'occurred_at': '2026-11-13T10:00:00Z'}]}
class DomainTests(unittest.TestCase):
 def test_future_plan_cannot_fill_occurrence(self):
  x=run(DEMO);self.assertEqual({r['code']for r in x['findings']},{'non_occurred_event_has_occurrence','future_occurrence'})
 def test_past_plan_still_not_occurrence(self):
  x=copy.deepcopy(DEMO);x['events'][0]['target_at']='2026-11-10T10:00:00Z';del x['events'][0]['occurred_at'];self.assertTrue(run(x)['valid'])
 def test_timezone_not_assumed(self):
  with self.assertRaises(ValueError):run(dict(DEMO,now='2026-11-12T12:00:00'))
