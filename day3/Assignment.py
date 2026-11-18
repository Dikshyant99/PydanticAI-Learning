from dataclasses import dataclass
from datetime import date
from typing import Literal
from pydantic_ai import Agent
from pydantic import BaseModel,Field
from pydantic_ai.messages import ToolCallPart,ToolReturnPart
from dotenv import load_dotenv

load_dotenv()

#Output model
class Assignment(BaseModel):
    title:str=Field(description='Short name of the assignment')
    subject:str=Field(description='subject code')
    due_date: date
    days_left:int=Field(description='Days left until the due date,from the day untill tool')
    weight_percent:int | None=Field(description='Grade weight from get_subject_weight,or none if unknown')
    priority: Literal['low','medium','high']
    task:list[str]=Field(description='concrete steps needed to finish the task')
    
    
#Agent
agent=Agent(
    'anthropic:claude-haiku-5-5',
    output_type=Assignment,
    instructions=(f'Extract the assignment details from the student message. Today is {date.today()}. '
        'Use the tools to get days_left and the grade weight; never calculate or guess them. '
        'Priority rule: high if weight >= 25 or days_left <= 3, low if weight < 10, otherwise medium.'
    ),
    )
#Tools
#Fake data of the ASSIGNMENT weightage
SUBJECT_WEIGHT={
    'DBMS':30,
    'OOP':20,
    'NETWORKING':15,
    'ENGLISH':5,
}

@agent.tool_plain
def days_until(due:date)->int:
    """Return the exact number of days from today until the given due date."""
    print(f'   [tool] days_until({due})')
    return (due - date.today()).days

@agent.tool_plain
def get_subject_weight(subject:str)->int | None:
    """Return how many percent of the final grade this subject's assignment is worth.

    Use the short subject code, e.g. 'DBMS'. Returns None if the subject is unknown.
    """
    print (f'[tool]get_subject_weignt({subject!r})')
    return SUBJECT_WEIGHT.get(subject)

#Run it
message=(
    "ugh I have to finish the database project for DBMS by next Friday, "
    "need to design the ER diagram, write the SQL tables and make slides.")
print('running agent...')
result=agent.run_sync(message)

a=result.output
print('\n--- Result ---')
print('Title:    ', a.title)
print('Subject:  ', a.subject)
print('Due:      ', a.due_date, f'({a.days_left} days left)')
print('Weight:   ', a.weight_percent, '%')
print('Priority: ', a.priority)
print('Tasks:')

for i, task in enumerate(a.task, start=1):
    print(f'{i}.{task}')
    
    





    
    
    

    



