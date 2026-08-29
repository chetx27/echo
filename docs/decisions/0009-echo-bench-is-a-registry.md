# Decision: ECHO-Bench is a local task registry

**Decision:** Keep an in-repo registry (`echo.bench`) of sequential-discovery tasks with a named question, primary metric, and config path.

**Reason:** Experiments 1–5 plus the new worlds need a single index so configs do not silently drift from the questions they claim to answer.

**Alternatives:** A public leaderboard; a pip-installable benchmark package; delaying any registry until ocean data exists.

**Rejected because:** Calling this a community benchmark would be a marketing claim. There is no held-out hidden test server and no leakage audit beyond the existing policy/environment split.

**Consequences:** `python -m echo bench` lists tasks. Numbers still come from `summary.json`. Do not write that ECHO-Bench is a standard.
