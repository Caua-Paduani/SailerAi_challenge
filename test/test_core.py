import pytest 
from unittest.mock import patch, MagicMock
import json
from SailerAi_challenge.tools import CRMtool, RAGtool, KnowledgeAugmentationTool
from SailerAi_challenge.llm import analyze_message, decide_tool_usage, synthesize_results


@pytest.fixture
def mock_llm_client():
    response = MagicMock()
    with patch("SailerAi_challenge.llm.llm_client.generate_response", return_value=response):
        crm_tool = MagicMock()
        rag_tool = MagicMock()
        knowledge_tool = KnowledgeAugmentationTool()
        yield crm_tool, rag_tool, knowledge_tool
        
