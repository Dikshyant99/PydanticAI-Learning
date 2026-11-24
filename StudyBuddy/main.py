"""Terminal version of Study Buddy.

Run it with:  python StudyBuddy/main.py
"""
from agent import StudyDeps, agent
from storage import load_assignments


#The chat loop
def main() -> None:
    name = input("What's your name? ").strip()
    deps = StudyDeps(student_name=name, assignments=load_assignments())  # One backpack, filled from the saved file
    history = []  # Conversation memory

    print(f"Hi {name}! Study Buddy is ready. Type quit to exit.")
    print(f"(Loaded {len(deps.assignments)} saved assignment(s).)\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue  # Skip empty lines instead of sending them to the model
        if user_input.lower() == 'quit':
            print("Study Buddy: Bye! Good luck with your work.")
            break
        try:
            result = agent.run_sync(user_input, deps=deps, message_history=history)
        except Exception as e:
            # Network/API problems: show the error and keep chatting
            print(f"Study Buddy: Sorry, something went wrong ({e}). Please try again.\n")
            continue
        history = result.all_messages()
        print(f"Study Buddy: {result.output}\n")


if __name__ == '__main__':
    main()
    
    

