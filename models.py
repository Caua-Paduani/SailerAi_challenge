from typing import List,Dict ,Optional, Any
from pydantic import BaseModel,Field
from datetime import datetime
# Define the Message model for the conversation history
class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime.now = Field(default_factory = datetime.now)
# Define the ConversationRequest model
class ConversationRequest(BaseModel):
    conversation_history: List[Message]
    current_prospect_message: Message
    prospect_id: Optional[str] = None
    
# Define the ActionableOutput model for the response
class ActionableOutput(BaseModel):
    actionable_insights: str
    suggested_reply: str
    next_steps: List[str]
    additional_context: Optional[Dict[str, Any]] = None

#get intent from the message using the intent classifier
class Intent(BaseModel):
    intent_type: str
    confidence_score: float
    additional_context: Optional[Dict[str, Any]] = None
    
#analyze the message using the analysis model
class AnalysisResult(BaseModel):
    analysis_type: str
    analysis_result: str
    