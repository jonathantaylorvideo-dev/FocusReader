\# FocusReader Sandbox Setup



\## Container Invocation

\- \*\*Build Command:\*\* `docker build -t agentic\_engineer\_1 .`

\- \*\*Run Command:\*\* `docker run -it --rm -v "${PWD}:/workspace" agentic\_engineer\_1`



\## Security Boundaries \& Volume Mounting

\- \*\*Mounted Directory:\*\* Only the `FocusReader` project directory (`/workspace`) is mounted from the host. This restricts the agent's file system visibility and prevents access to sensitive host directories.

\- \*\*Ephemeral Files:\*\* Temporary cache files (`\_\_pytest\_cache\_\_`, `\_\_pycache\_\_`) and runtime execution outputs are kept ephemeral or ignored to prevent repo clutter.

\- \*\*Persisted Files:\*\* Core source modules (`schema\_validator.py`, `orchestrator.py`), the test suite (`tests/test\_pipeline.py`), and the data pipeline directories (`Inbox`, `Processed`, `Quarantine`) persist on the host filesystem via volume binding.



\## Smoke Test Results

\- \*\*Command:\*\* `python -m pytest -v`

\- \*\*Result:\*\* All 4 unit and integration tests passed successfully, confirming proper schema validation and file routing within the container boundary.

