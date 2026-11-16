from datetime import date
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


class Assignment(BaseModel):
    title: str = Field(description='Short name of the assignment')
    subject: str
    due_date: date
    priority: Literal['low', 'medium', 'high']
    tasks: list[str] = Field(description='Concrete steps needed to finish it')


agent = Agent(
    'anthropic:claude-haiku-5-5',
    output_type=Assignment,
    instructions=f'Extract the assignment details from the student message. Today is {date.today()}.',
)

message = (
    "ugh I have to finish the database project for DBMS by next Friday, "
    "need to design the ER diagram, write the SQL tables and make slides. "
    "it's worth 30% so it's really important"
)

result = agent.run_sync(message)

assignment = result.output
print(type(assignment))
print('Title:   ', assignment.title)
print('Subject: ', assignment.subject)
print('Due:     ', assignment.due_date)
print('Priority:', assignment.priority)
print('Tasks:')

for i, task in enumerate(assignment.tasks, start=1):
    print(f'  {i}. {task}')

days_left = (assignment.due_date - date.today()).days
print(f'\nDays left: {days_left}')