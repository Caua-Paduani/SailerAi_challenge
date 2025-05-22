from fastapi import FastAPI, HTTPException
from models import ConversationRequest, ActionableOutput
from processor import process_message
#create the FastAPI app
app = FastAPI(
    title="Sailer AI , Sales Assistant",
    description = "An API for processing sales and AI interaction",
    version = "1.0.0"
)
#endpoint for processing messages
@app.post("/process_message", response_model=ActionableOutput)
async def process_conversation(request: ConversationRequest):
     """
    Process a new message from a prospect.
    
    Accepts:
    - conversation_history: A list of previous messages in the conversation
    - current_prospect_message: The latest message from the prospect
    - prospect_id:  Identifier for the prospect
    
    Returns a structured response with analysis and suggested reply.
    """
try: 
        response = process_message(request)
        return response.json()
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    

