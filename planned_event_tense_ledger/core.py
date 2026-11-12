from datetime import datetime,timezone
from .common import unique_ids
def instant(value):
 if not isinstance(value,str):raise ValueError('instant')
 dt=datetime.fromisoformat(value.replace('Z','+00:00'))
 if dt.tzinfo is None:raise ValueError('timezone_required')
 return dt.astimezone(timezone.utc)
def run(data):
 now=instant(data['now']);events=data['events']
 if not isinstance(events,list)or len(events)>10000:raise ValueError('events')
 unique_ids(events);findings=[]
 for row in events:
  kind=row['kind']
  if kind not in ['planned','occurred','cancelled']:raise ValueError('kind')
  target=instant(row['target_at'])if row.get('target_at')else None;occurred=instant(row['occurred_at'])if row.get('occurred_at')else None
  if kind=='planned'and target is None:findings.append({'id':row['id'],'code':'missing_target_time'})
  if kind in ['planned','cancelled']and occurred is not None:findings.append({'id':row['id'],'code':'non_occurred_event_has_occurrence'})
  if kind=='occurred'and occurred is None:findings.append({'id':row['id'],'code':'missing_occurrence_time'})
  if occurred is not None and occurred>now:findings.append({'id':row['id'],'code':'future_occurrence'})
 return {'findings':findings,'valid':not findings,'events_changed':False,'natural_language_extraction_performed':False}
