"""The Study Buddy agent and its tools.

No input()/print() here, so any frontend (terminal, FastAPI, ...) can import it.
"""
from dataclasses import dataclass, field
from datetime import date

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

from models import Assignment
from storage import find_assignment, save_assignments

load_dotenv()


#The dependencies that are handed to the agent on every run.
#field(default_factory=list) gives each backpack its OWN empty list.
#(A plain "= []" would share one list between all backpacks.)
@dataclass
class StudyDeps:
    student_name: str
    assignments: list[Assignment] = field(default_factory=list)


#Creating the agent, the deps_type tells the agent which deps_type to expect
agent = Agent(
    'anthropic:claude-haiku-5-5',
    deps_type=StudyDeps,
    instructions=(
        'You are Study Buddy, a friendly assistant that helps students '
        'manage their assignments. Keep replies short and encouraging. '
        'Always use the tools to add, list, complete or delete assignments. '
        'Never make up assignments that are not in the list.'
    ),
)


#Dynamic instructions: This runs on every turn, so the date is always fresh and it can access the backpack(ctx.deps)
@agent.instructions
def add_student_context(ctx: RunContext[StudyDeps]) -> str:
    today = date.today()
    return f"You are helping {ctx.deps.student_name}. Today is {today:%A}, {today}."


#Tools @agent.tool as they need ctx
#the model never sees the ctx they see other arguments
@agent.tool
def add_assignment(ctx: RunContext[StudyDeps], title: str, subject: str, due_date: date) -> str:
    "Add a new assignment to the student's list."
    if find_assignment(ctx.deps.assignments, title):
        return f"An assignment called '{title}' already exists. Use a different title."
    new = Assignment(title=title, subject=subject, due_date=due_date)
    ctx.deps.assignments.append(new)
    save_assignments(ctx.deps.assignments)
    return f"Added '{title}' ({subject}), due {due_date}."


@agent.tool
def list_assignment(ctx: RunContext[StudyDeps]) -> list[dict] | str:
    """List all of the student's assignments with due date, days left and status."""
    if not ctx.deps.assignments:
        return 'The student has no assignments.'
    today = date.today()
    return [
        {
            'title': a.title,
            'subject': a.subject,
            'due_date': a.due_date.isoformat(),
            'days_left': (a.due_date - today).days,  # code does the maths, not the model
            'done': a.done,
        }
        for a in ctx.deps.assignments
    ]


@agent.tool
def mark_done(ctx: RunContext[StudyDeps], title: str) -> str:
    "Mark the assignment as done, use the assignment's title."
    a = find_assignment(ctx.deps.assignments, title)
    if a is None:
        return f"No assignment called '{title}'. Check the list for the exact title."
    a.done = True
    save_assignments(ctx.deps.assignments)
    return f"Marked '{a.title}' as done."

@agent.tool
def delete_assignment(ctx: RunContext[StudyDeps], title: str) -> str:
    "Delete an assignment from the list, use the assignment's title."
    a = find_assignment(ctx.deps.assignments, title)
    if a is None:
        return f"No assignment called '{title}'. Check the list for the exact title."
    ctx.deps.assignments.remove(a)
    save_assignments(ctx.deps.assignments)
    return f"Deleted '{a.title}'."


