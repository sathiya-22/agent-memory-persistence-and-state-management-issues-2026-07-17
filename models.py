from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel, Field
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class AgentStateDB(Base):
    __tablename__ = 'agent_states'

    id = Column(Integer, primary_key=True)
    agent_id = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    state_json = Column(Text, nullable=False)

    def __repr__(self):
        return f"<AgentState(id={self.id}, agent_id='{self.agent_id}', timestamp='{self.timestamp}')>"

class AgentMemory(BaseModel):
    last_thought: Optional[str] = None
    conversation_history: list[str] = Field(default_factory=list)
    internal_data: Dict[str, Any] = Field(default_factory=dict)
    run_count: int = 0

class AgentPersistenceManager:
    def __init__(self, db_path="sqlite:///agent_memory.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_agent_state(self, agent_id: str, memory: AgentMemory):
        try:
            session = self.Session()
            existing_state = session.query(AgentStateDB).filter_by(agent_id=agent_id).first()

            state_data = memory.model_dump_json()

            if existing_state:
                existing_state.state_json = state_data
                existing_state.timestamp = datetime.utcnow()
            else:
                new_state = AgentStateDB(agent_id=agent_id, state_json=state_data)
                session.add(new_state)
            
            session.commit()
            session.close()
            logger.info(f"Saved state for agent '{agent_id}'.")
        except Exception as e:
            logger.error(f"Failed to save state for agent '{agent_id}': {str(e)}")

    def load_agent_state(self, agent_id: str) -> Optional[AgentMemory]:
        try:
            session = self.Session()
            state_record = session.query(AgentStateDB).filter_by(agent_id=agent_id).first()
            session.close()

            if state_record:
                logger.info(f"Loaded state for agent '{agent_id}'.")
                return AgentMemory.model_validate_json(state_record.state_json)
            logger.info(f"No state found for agent '{agent_id}'.")
            return None
        except Exception as e:
            logger.error(f"Failed to load state for agent '{agent_id}': {str(e)}")
            return None
