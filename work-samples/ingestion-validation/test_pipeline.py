import tempfile
import unittest
from pathlib import Path
from pipeline import ingest

class PipelineTests(unittest.TestCase):
 def test_replay_and_quarantine(self):
  with tempfile.TemporaryDirectory() as tmp:
   db=Path(tmp)/'data.db'
   rows=[{'id':'a','updated_at':'2026-11-01T00:00:00+00:00','amount':12}, {'id':'bad','amount':'x'}]
   self.assertEqual(ingest(rows,db)['accepted'],1)
   self.assertEqual(ingest(rows,db)['accepted'],0)
   self.assertEqual(ingest([{'id':'a','updated_at':'2026-11-02T00:00:00+00:00','amount':20}],db)['accepted'],1)
 def test_out_of_order_does_not_regress(self):
  with tempfile.TemporaryDirectory() as tmp:
   db=Path(tmp)/'data.db'
   ingest([{'id':'a','updated_at':'2026-11-02T00:00:00+00:00','amount':20}],db)
   self.assertEqual(ingest([{'id':'a','updated_at':'2026-11-01T00:00:00+00:00','amount':10}],db)['accepted'],0)

if __name__=='__main__': unittest.main()
