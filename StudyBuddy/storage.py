"""Storage: loading and saving assignments.

Right now this uses a JSON file. Later you can swap it for SQLite
without changing agent.py or api.py, as long as these functions keep
the same names and arguments.
"""
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from models import Assignment

#Saving to a file so assignments survive after you quit.
#The file sits next to this file, whatever folder you run the script from.
DATA_FILE = Path(__file__).parent / 'assignments.json'

#A TypeAdapter lets Pydantic convert a whole list[Assignment] to JSON and back.
assignment_list = TypeAdapter(list[Assignment])


def load_assignments() -> list[Assignment]:
    "Read saved assignments from the file (an empty list if there is no file yet)."
    if not DATA_FILE.exists():
        return []
    try:
        return assignment_list.validate_json(DATA_FILE.read_bytes())
    except ValidationError:
        # The file is damaged or in the wrong format: start fresh instead of crashing
        print(f"(Could not read {DATA_FILE.name}, starting with an empty list.)")
        return []


def save_assignments(assignments: list[Assignment]) -> None:
    "Write all assignments to the file, replacing what was there."
    DATA_FILE.write_bytes(assignment_list.dump_json(assignments, indent=2))


def find_assignment(assignments: list[Assignment], title: str) -> Assignment | None:
    "Find an assignment by title, ignoring upper/lower case."
    for a in assignments:
        if a.title.lower() == title.lower():
            return a
    return None


