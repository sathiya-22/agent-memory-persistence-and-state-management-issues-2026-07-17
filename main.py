from agent import MyAgent
from models import AgentPersistenceManager
import os

def main():
    # Clean up previous DB for a fresh start each time
    if os.path.exists("agent_memory.db"):
        os.remove("agent_memory.db")
        print("Cleaned up previous 'agent_memory.db'.")

    persistence_manager = AgentPersistenceManager()
    agent_id = "my_first_agent"

    print("--- First Agent Run (Initializing or Loading State) ---")
    agent = MyAgent(agent_id, persistence_manager)
    agent.run("Hello agent, how are you?")
    
    print("\n--- Simulating Agent Shut Down and Restart ---")
    # Simulate a new process or restart by creating a new agent instance
    # The new instance should load the previously saved state
    restarted_agent = MyAgent(agent_id, persistence_manager)
    restarted_agent.run("What did we talk about last time?")

    print("\n--- Another Agent Run ---")
    restarted_agent.run("Can you remember this new piece of information?")

    print("\n--- Final Agent State After All Runs ---")
    print(restarted_agent.memory.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
