# Incremental ingestion and validation â€” local prototype

Synthetic independently written educational example. This is a local ingestion component, **not a deployed Azure pipeline** and not employer work. Candidate must understand and extend it before presenting it as a work sample.

Python 3.11+; no dependencies. From this folder:
```
python -m unittest discover
python pipeline.py --input sample.json --database demo.db
python pipeline.py --input sample.json --database demo.db
```
First run: two accepted, one rejected, two total. Replay: zero accepted, one rejected, two total. Invalid records go to SQLite quarantine. Newer updates replace existing rows; older/equal events cannot regress state. Entire batch is transactional. Equal timestamps with changed payload are deliberately ignored; production must define source sequencing or conflict handling.

Local architecture: synthetic JSON -> schema/time/value validation -> quarantine OR timestamp-guarded SQL upsert. No network, secrets or employer code.

Azure completion checklist (not yet implemented): ADF source extraction to immutable Blob landing paths; managed identity and least-privilege access; Azure SQL staging/upsert; persisted extraction watermark advanced only after successful load; bounded transient retries; monitoring and poison-record alert. Add integration tests and a screenshot/demo of an actual sandbox execution before calling this Azure-deployed. No paid resources are provisioned by this example.

Demo narration: show synthetic input, run twice, explain why replay is safe, query quarantine, introduce a newer record then an older record, explain the difference between source watermark and sink idempotency. Discuss API pagination, late arrivals and retention as next design decisions.
