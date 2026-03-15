from agent import ResearchAgent

agent = ResearchAgent()

def main():

    print("Research Agent (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        
        if user_input in ["exit", "quit"]:
            break

        answer = agent.run(user_input)

        print("\nAgent:", answer)

if __name__ == "__main__":
    main()