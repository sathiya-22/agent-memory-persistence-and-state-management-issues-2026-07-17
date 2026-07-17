from models import AgentMemory, AgentPersistenceManager
import time

class MyAgent:
    def __init__(self, agent_id: str, persistence_manager: AgentPersistenceManager):
        self.agent_id = agent_id
        self.persistence_manager = persistence_manager
        self.memory: AgentMemory = self._load_or_initialize_memory()

    def _load_or_initialize_memory(self) -> AgentMemory:
        loaded_memory = self.persistence_manager.load_agent_state(self.agent_id)
        if loaded_memory:
            return loaded_memory
        return AgentMemory(conversation_history=["Agent initialized."])

    def run(self, input_message: str):
        print(f"\n--- Agent '{self.agent_id}' Run ---")
        self.memory.run_count += 1
        print(f"Run count: {self.memory.run_count}")

        # Simulate agent processing
        self.memory.conversation_history.append(f"User: {input_message}")
        thought = f"Thinking about '{input_message}' at run {self.memory.run_count}..."
        self.memory.last_thought = thought
        self.memory.conversation_history.append(f"Agent: {thought}")
        self.memory.internal_data[f"status_run_{self.memory.run_count}"] = "processed"

        print(f"Current Memory:\n{self.memory.model_dump_json(indent=2)}")
        
        # Persist state after each run
        self.persistence_manager.save_agent_state(self.agent_id, self.memory)
        print(f"Agent '{self.agent_id}' finished run {self.memory.run_count}.")
