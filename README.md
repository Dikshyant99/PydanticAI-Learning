# PydanticAI Learning

My notes and practice code from learning [Pydantic AI](https://ai.pydantic.dev/), which I used to build AI agents in Python with Claude models. Each folder covers one concept, and they build up to **Study Buddy**, a chatbot that manages student assignments.

## What's inside

| Folder | Concept | What it does |
|---|---|---|
| `Day1/` | Structured output | Turns a messy student message ("finish the DBMS project by next Friday...") into a validated `Assignment` object with a title, subject, due date, priority and tasks |
| `day2/` | Tools, dependencies and dynamic instructions | A study planner that looks up assignments and due dates through tools instead of guessing, and greets the student by name |
| `day3/` | Tools + structured output together | Extracts an assignment and uses tools to get the days left and grade weight, then picks a priority from fixed rules |
| `weatherTool/` | Real APIs, `ModelRetry` and cost tracking | Compares the weather in two cities with the free Open-Meteo API, gives packing advice, and prints the token usage and cost of each run |
| `StudyBuddy/` | Full project | A terminal chatbot that adds, lists and completes assignments, remembers the conversation and saves assignments to a JSON file |

## Study Buddy

```
StudyBuddy/
├── main.py      # terminal chat loop
├── agent.py     # the agent and its tools (add, list, mark done)
├── models.py    # Pydantic data models
├── storage.py   # load/save assignments to assignments.json
├── api.py       # FastAPI version (in progress)
└── static/      # web frontend (in progress)
```

The agent code doesn't use `input()` or `print()`, so the same agent can run behind the terminal or behind a FastAPI web app.

**Coming next:** REST endpoints for assignments, a `/chat` endpoint and a simple web UI.

## Setup

1. Clone the repo and create a virtual environment:
   ```
   git clone https://github.com/Dikshyant99/PydanticAI-Learning.git
   cd PydanticAI-Learning
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   ```
2. Install the packages:
   ```
   pip install pydantic-ai python-dotenv httpx
   ```
3. Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Running

```
python Day1/main.py
python day2/main.py
python day3/Assignment.py
python weatherTool/main.py
python StudyBuddy/main.py
```

Example Study Buddy chat:

```
What's your name? Dikshyant
Hi Dikshyant! Study Buddy is ready. Type quit to exit.

You: add my OS lab report, due next Monday
Study Buddy: Added 'OS Lab Report' (OS), due 2026-11-30. You've got this!
You: what do I have left?
```

## Key things I learned

- **Structured output:** setting `output_type` to a Pydantic model means the agent returns validated data, not free text.
- **Tools:** the model calls Python functions for facts like dates and lookups, so it doesn't make them up.
- **Dependencies (`deps`):** you pass app data into each run without putting it in global variables.
- **Message history:** this is how a chatbot remembers earlier turns.
- **Cost tracking:** I read token usage from each run and turned it into a cost estimate.

## Tech

Python · Pydantic AI · Pydantic · Claude (Anthropic) · httpx · Open-Meteo API
