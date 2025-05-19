from typing import List,Dict ,Optional, Any
from pydantic import BaseModel,Field
from datetime import datetime
# Define the Message model
class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime.now = Field(default_factory = datetime.now)
# Define the ConversationRequest model
class ConversationRequest(BaseModel):
    conversation_history: List[Message]
    current_prospect_message: Message
    prospect_id: Optional[str] = None
    
# Define the ActionableOutput model
class ActionableOutput(BaseModel):
    actionable_insights: str
    suggested_reply: str
    next_steps: List[str]
    additional_context: Optional[Dict[str, Any]] = None
    
    
