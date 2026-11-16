from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()
agent=Agent(
    'anthropic:claude-opus-4-8',
    
instructions='You are a java tutor and need to explain the difference between simple java class and object using java code',
)
result= agent.run_sync("Explain difference between class and object")
result2=agent.run_sync("explain oop")
print(result2.output)

 

