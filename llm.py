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



def decide_tool_usage(analysis_result: Dict, conversation_history: List[Dict], current_prospect_message: str) -> Dict:
    """
    Decide if the KnowledgeAugmentationTool should be called to gather more information.
    
    Args:
        analysis_result: The analysis from analyze_message()
        conversation_history: List of previous messages
        current_prospect_message: The latest message from the prospect
        
    Returns:
        Decision about tool usage as a dictionary
    """
    formatted_conversation = "\n".join([
        f"{msg['sender']}: {msg['content']}"
        for msg in conversation_history
    ])
    
    prompt = f"""
    You are an AI sales assistant deciding whether to use the KnowledgeAugmentationTool to gather more information or perform actions.

    CONVERSATION HISTORY:
    {formatted_conversation}

    CURRENT PROSPECT MESSAGE:
    {current_prospect_message}
    
    ANALYSIS RESULT:
    {json.dumps(analysis_result, indent=2)}
    
    The KnowledgeAugmentationTool can retrieve information from:
    1. CRM data - Information about the prospect (company size, previous interactions, technologies used)
    2. Knowledge base - Product documentation, pricing, sales playbooks, competitor comparisons
    
    Decide if you need additional information to respond effectively.
    
    Return your decision as a JSON object with exactly this structure:
    {{
        "needs_information": True or False,
        "information_type": "crm_data" or "knowledge_base" or null,
        "information_parameters": {{
            // For crm_data:
            "prospect_id": "string",
            "fields_needed": ["company_size", "technologies_used", "pain_points"],
            
            // OR for knowledge_base:
            "query": "specific search query",
            "document_types": ["pricing", "product", "sales_playbook", "competitor"],
            "related_entities": ["specific product", "feature"]
        }},
        "reason": "string explaining why this information is needed or not needed"
    }}
    
    Only set information_type and information_parameters if needs_information is true.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI sales assistant deciding if additional information is needed."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    return json.loads(response.choices[0].message.content)