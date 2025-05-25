
from models import ConversationRequest, ActionableOutput
from llm import analyze_message, decide_tool_usage, synthesize_results
from tools import KnowledgeAugmentationTool

async def process_message(request: ConversationRequest) -> ActionableOutput:
    """
    Process a new prospect message and generate a response
    
    Args:
        request: The ConversationRequest object containing conversation history and current message
        
    Returns:
        ActionableOutput with analysis and response
    """
    tool_usage_results = {}
    #converts pydantic object to a dictionary
    conversation_history = [
        {
            "sender": msg.sender,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in request.conversation_history
    ]
    analysis_result= analyze_message(conversation_history = conversation_history,
    current_prospect_message = request.current_message)

    info_decision = decide_tool_usage(analysis_result = analysis_result,
conversation_history = conversation_history,
current_prospect_message = request.current_prospect_message)
    
    tool_decision = {}
    if info_decision.get("needs_information",False):
        knowledge_tool = KnowledgeAugmentationTool()
        info_type = info_decision.get("information_type")
        info_parameters = info_decision.get("information_parameters",{})

        if info_type == "crm_data":
            tool_decision["tool_name"] = "fetch_prospect_details"
            tool_params = {
                "prospect_id": info_parameters.get("prospect_id"),
                "fields_needed": info_parameters.get("fields_needed",[])
            }
        elif info_type == "knowledge_base":
            tool_decision["tool_name"] = "query_knowledge_base"
            tool_params = {
                "query": info_parameters.get("query"),
                "document_types":info_parameters.get("document_types",[]),
                "related_entities":info_parameters.get("related_entities",[])
            }
        else:
            tool_name = None
            tool_params = {}

        if tool_name:
            tool_results = {}
            # execute the tool
            execution_result = knowledge_tool.execute(tool_name = tool_name, tool_params = tool_params)
            if execution_result.get("success",False):
            #store the result
                tool_results[info_type] = execution_result.get("output_result",{})
            else:
                tool_results[info_type] = {
                    "error": execution_result.get("error_message","Tool execution failed")
                }

        final_response = synthesize_results(analysis_result = analysis_result,
                                            conversation_history = conversation_history,
                                            current_prospect_message = request.current_prospect_message.content,
                                            tool_usage_results = tool_usage_results)
        
        return ActionableOutput(
            detailed_analysis = final_response.get("detailed_analysis",""),
            suggested_response_draft = final_response.get("suggested_response_draft",""),
            internal_next_steps = final_response.get("internal_next_steps",[]),
            tool_usage_log = final_response.get("tool_usage_log",{}),
            confidence_score = final_response.get("confidence_score",0.0),
            reasoning_trace = final_response.get("reasoning_trace","")
        )
    
  
     