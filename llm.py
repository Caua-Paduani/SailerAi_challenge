import os 
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict,List
import json
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4"

def analyze_message(conversation_history: List[Dict], current_prospect_message:str) -> Dict:
    """
     Use the LLM to analyze the prospect's message in context.
    
    Args:
        conversation_history: List of previous messages
        current_prospect_message: The latest message from the prospect
        
    Returns:
        Analysis result as a dictionary
    """
    formatted_conversation = "\n".join([
        f"{msg['sender']}: {msg['content']}"
        for msg in conversation_history
    ])
    prompt = f"""
    You are an AI sales assistant analyzing a prospect's message in the context of a sales conversation.

    CONVERSATION HISTORY:
    {formatted_conversation}

    CURRENT PROSPECT MESSAGE:
    {current_prospect_message}
    
     
   Analyze this message and extract:
   1. Intent (inquiry, objection, buying signal, etc.)
   2. Key entities mentioned (products, features,specific pain points, etc.)
   3. Overall sentiment (positive, negative, neutral)
   4. Key points that need addressing
   
   Format your response as a JSON object with this structure:
   {{
       "intent": {{...}},
       "entities": [...],
       "sentiment": "...",
       "key_points": [...]
   }}
   """

    response = client.chat.completions.create(
       model=MODEL,
       messages = [
           {
               "role": "system","content":"You are an AI sales assistant analyzing a prospect's message in the context of a sales conversation.",
               "role": "user","content":prompt
           }
       ],
       response_format={"type": "json_object"},
       temperature=0.3
)
    return json.loads(response.choices[0].message.content)

