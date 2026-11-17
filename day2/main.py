from dataclasses import dataclass
from datetime import date,timedelta
from dotenv import load_dotenv
from pydantic_ai import Agent , RunContext
from pydantic_ai.messages import ToolCallPart

load_dotenv()

#Dependencies: The data your app hands to the agent in each run
@dataclass
class StudentDeps:
    name:str
    assignment: dict[str,date] # due date
    
# the agent knows which dept type to expect
agent=Agent( 'anthropic:claude-haiku-5-5',
            deps_type=StudentDeps,
            instructions=('you are a study planner for the students, always use the tools to look up to the dates and assignments.Never guess the dates'),
            )
#Dynamic Instructions: The instructions build from the deps at runtime
@agent.instructions
def student_name(ctx:RunContext[StudentDeps])->str:
    return f"The student's name is {ctx.deps.name}. Address them by name."
    
#Plain tool : Needs no context
@agent.tool_plain
def get_today()->str:
    "Return todays date in yyyy-mm-dd format."
    return date.today().isoformat()
#context tool : Reads the student data from the deps
@agent.tool
def list_assignments(ctx:RunContext[StudentDeps])->dict[str,str]:
    "Return all of the student's assignments with their due dates (YYYY-MM-DD)."
    return {
        title: due.isoformat() for title, due in ctx.deps.assignment.items()
    }
#Plain tool with an argument : Pydantic validates the date the model sends
@agent.tool_plain
def days_until (due_date:date)->int:
    "Return how many days from today until due_date. Negative means overdue."
    return (due_date - date.today()).days

today = date.today()
deps=StudentDeps(
    name='Dikshyant Karki',
    assignment={
       'DBMS ER DIAGRAM': today + timedelta(days=3),
       'OS LAB REPORT': today + timedelta(days=8),
       'AI ESSAY': today + timedelta(days=1),
       
    },
)

result = agent.run_sync(
    'Which assignment should i start first and how many days do i have to complete each assignment?',
    deps=deps,
)
print("===ANSWERS===")
print(result.output)

#See which tools the model actually calls
print('\n====Tools Called====')
for message in result.all_messages():
    for part in message.parts:
        if isinstance(part,ToolCallPart):
            print('-> {part.tool_name}({part.args})')
            
            

    



    
    

