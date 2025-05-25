import os 
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict,List,Optional
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

def synthesize_results(analysis_result: Dict, conversation_history: List[Dict], current_prospect_message: str,tool_usage_results: Optional[Dict] = None) -> Dict:
    """
    Synthesize all information into a final structured response.
    
    Args:
        analysis_result: The initial analysis from analyze_message()
        conversation_history: List of previous messages
        current_prospect_message: The latest message from the prospect
        tool_usage_results: Results from any tools that were called (optional)
        
    Returns:
        Structured final response with analysis, suggested response, next steps, etc.
    """
    formatted_conversation = "\n".join([
        f"{msg['sender']}: {msg['content']}"
        for msg in conversation_history
    ])

    tool_usage_info = "No tools were used"
    if tool_usage_results:
        tool_name = tool_usage_results.get("tool_name")
        params = tool_usage_results.get("tool_params")
        success = tool_usage_results.get("success",False)
        output = tool_usage_results.get("output_result")
        tool_usage_info =f"""Tool: {tool_name}
        Parameters: {params}
        Success: {success}
        Output: {output}
        """


    prompt = f"""
    You are an AI sales assistant synthesizing a final response  based on all available information.

    CONVERSATION HISTORY:
    {formatted_conversation}

    CURRENT PROSPECT MESSAGE:
    {current_prospect_message}

    ANALYSIS RESULT:
    {json.dumps(analysis_result, indent=2)}

    TOOL USAGE RESULTS:
    {tool_usage_info}
    
     
    Based on all this information, generate a comprehensive response in the following JSON format:
    {{
        "detailed_analysis": "A thorough summary of your understanding of the prospect's message and context",
        "suggested_response_draft": "A concise, helpful, and contextually appropriate response to the prospect",
        "internal_next_steps": [
            {{"action": "ACTION_TYPE", "details": {{"key": "value"}}}},
            ...
        ],
        "tool_usage_log": {{
            "tools_used": ["tool_name"] or [],
            "inputs": {{}},
            "output_summary": "Brief summary of tool outputs"
        }},
        "confidence_score": An estimated confidence score between 0.0 and 1.0 in the suggested_response_draft and internal_next_steps,
        "reasoning_trace": "Brief explanation of why you chose certain tools or formulated this response"
    }}
    
    Make sure the suggested_response_draft is professional, addresses the prospect's needs directly, and leverages any information retrieved from tools.
    The internal_next_steps should be practical actions for the sales team to take.
    The confidence_score should reflect how certain you are that your response is appropriate and helpful.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI sales assistant synthesizing a final response."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)

