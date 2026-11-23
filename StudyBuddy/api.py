"""FastAPI app for Study Buddy (to be written).

Setup:
    pip install "fastapi[standard]"
Run (from inside the StudyBuddy folder):
    fastapi dev api.py
Then open http://127.0.0.1:8000/docs to try your endpoints.

Plan:
    1. Assignment endpoints (no AI yet), test them in /docs:
         GET    /assignments          -> list all
         POST   /assignments          -> add one (request body: Assignment)
         PATCH  /assignments/{title}  -> mark as done
         DELETE /assignments/{title}  -> delete
       Reuse load_assignments / save_assignments / find_assignment from storage.py.

    2. Chat endpoint:
         POST /chat  -> body: {"message": "..."}, returns the agent's reply
       Use `await agent.run(...)` (async), not run_sync.

    3. Serve the frontend in static/ (look up StaticFiles in the FastAPI docs).

Topics to research: path operations, path & query parameters, request body,
response_model, HTTPException & status codes, async def, Depends, StaticFiles, CORS.
"""
