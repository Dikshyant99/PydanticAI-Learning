from dataclasses import dataclass
from pydantic_ai import Agent
from dotenv import load_dotenv


load_dotenv()

#Creating the agent
agent=Agent (
    'anthropic:claude-haiku-5-5',
    instructions=('Yoy are Study Buddy, a friendly assistant that helps the students'
                  'manages their assignments. Keep the replies short and encouraging'),
)
result=agent.run_sync("Hi my name is Dikshyant!")
print(result.output)
print("Study Buddy is  ready! Type 'quit' to exit.\n")

history=[]


while True:
    user_input=input('You:')

    if user_input.lower()=='quit':
        print("Study Buddy: Bye! GoodLuck with you work.")
        break
    
    result=agent.run_sync(user_input,message_history=history)
    history=result.all_messages()
    
    print(f'study Buddy:{result.output}')
    
    
    
    
 