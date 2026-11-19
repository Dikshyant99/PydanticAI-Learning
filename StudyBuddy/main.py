from dataclasses import dataclass , field
from pydantic_ai import Agent,RunContext
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import date



load_dotenv()
#What one assignment looks like
class  Assignment(BaseModel):
    title: str
    subject:str
    due_date: date
    done:bool=False # Every new assignment starts as not done

#The dependencies that are handed to the agent on every run.
#field(default_factory=list) gives each backpack its OWN empty list.
#(A plain "= []" would share one list between all backpacks.)

@dataclass

class StudyDeps:
    student_name=str
    assignments: list[Assignment] = field(default_factory=list)
    
    
    
    

#Creating the agent, the deps_type tells the agent which deps_type to expect
agent = Agent(
    'anthropic:claude-haiku-5-5',
    deps_type=StudyDeps,
    instructions=(
        'You are Study Buddy, a friendly assistant that helps students '
        'manage their assignments. Keep replies short and encouraging. '
        'Always use the tools to add, list or complete assignments. '
        'Never make up assignments that are not in the list.'
    ),
)

#Dynamic instructions: This runs on every turn, so the date is always fresh and it can acces the backpack(ctx.deps)
@agent.instructions
def add_student_context(ctx:RunContext[StudyDeps])->str:
    today=date.today()
    return f"you are helping {ctx.deps.student_name}.Today is {today:%A},{today}"

#Tools @agent.tool as they need ctx
#the model never sees the ctx they see other arguments

@agent.tool
def add_assignment(ctx:RunContext[StudyDeps],title:str,subject:str,due_date:date)->str:
    "Add a new assignment to the students list"
    new=Assignment(title=title,subject=subject,due_date=due_date)
    ctx.deps.assignments.append(new)
    return f"added '{title}',({subject}),{due_date}."

@agent.tool
def list_assignment(ctx:RunContext[StudyDeps])->list[dict] |str:
    """List all of the student's assignments with due date, days left and status."""
    if not ctx.deps.assignments:
        return 'the student has no assignments'
    today=date.today()
    return[{
        'title': a.title,
            'subject': a.subject,
            'due_date': a.due_date.isoformat(),
            'days_left': (a.due_date - today).days,  # code does the maths, not the model
            'done': a.done,
    }
           for a in ctx.deps.assignments
           ]
@agent.tool
def mark_done(ctx:RunContext[StudyDeps], title :str)->str:
    "Mark the assignment as done, use the assignments title"
    for a in ctx.deps.assignments:
        if a.title.lower()==title.lower():
            a.done = True
            return f"Marked'a.{title}' as done"
    return f"No assignment called '{title}'. Check the list for the exact title."

#The chat loop
def main()-> None:
    name=input("Whats your name?")
    deps= StudyDeps(student_name=name) # One backpack created once before the loop
    history=[] # Conversation memory (step1)
    
    print(f"HI,{name}! iam study buddy is ready.Type Quit to exit.\n")
    
    while True:
        user_input=input("YOU: ")
        if user_input.lower()=='quit':
            print("Study Buddy: BYE! GOODLUCK WITH YOUR WORK")
            
            break
        result=agent.run_sync(user_input,deps=deps,message_history=history)
        history=result.all_messages()
        print(f"Study Buddy:{result.output}\n")
        
        #Print (deps.assignments)
        
    if __name__=='main':
        main()
    
        
        
    
    

        
    
    


    



