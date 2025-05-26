import unittest
from datetime import datetime
from models import Message, ConversationRequest, ActionableOutput, Intent, AnalysisResult
from tools import CRMtool, RAGtool, KnowledgeAugmentationTool
import json
import os
import tempfile
import numpy as np

class TestModels(unittest.TestCase):
    """Unit tests for the data models"""
    
    def test_message_creation(self):
        """Test Message model creation and validation"""
        message = Message(
            sender="user",
            content="Hello",
            timestamp=datetime.now()
        )
        self.assertEqual(message.sender, "user")
        self.assertEqual(message.content, "Hello")
        self.assertIsInstance(message.timestamp, datetime)

    def test_conversation_request(self):
        """Test ConversationRequest model creation and validation"""
        history = [
            Message(sender="user", content="Hi"),
            Message(sender="assistant", content="Hello")
        ]
        current_message = Message(sender="user", content="How are you?")
        
        request = ConversationRequest(
            conversation_history=history,
            current_prospect_message=current_message,
            prospect_id="123"
        )
        
        self.assertEqual(len(request.conversation_history), 2)
        self.assertEqual(request.prospect_id, "123")
        self.assertEqual(request.current_prospect_message.content, "How are you?")

class TestCRMTool(unittest.TestCase):
    """Unit tests for the CRM tool"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = {
            "123": {
                "name": "Test User",
                "email": "test@example.com"
            }
        }
        
        # Create temporary CRM data file
        self.temp_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.temp_dir, "data"), exist_ok=True)
        self.crm_data_path = os.path.join(self.temp_dir, "data", "crm_data.json")
        
        with open(self.crm_data_path, "w") as f:
            json.dump(self.test_data, f)
            
        self.crm_tool = CRMtool()
        self.crm_tool.crm_data = self.test_data

    def test_fetch_prospect_details_success(self):
        """Test successful prospect details fetch"""
        result = self.crm_tool.fetch_prospect_details("123")
        self.assertTrue(result["prospect_found"])
        self.assertEqual(result["prospect_details"]["name"], "Test User")

    def test_fetch_prospect_details_not_found(self):
        """Test prospect details fetch for non-existent prospect"""
        result = self.crm_tool.fetch_prospect_details("999")
        self.assertFalse(result["prospect_found"])
        self.assertIn("error", result)

class TestRAGTool(unittest.TestCase):
    """Unit tests for the RAG tool"""
    
    def setUp(self):
        """Set up test data"""
        self.rag_tool = RAGtool()
        
        # Create test knowledge base directory and file
        self.temp_dir = tempfile.mkdtemp()
        self.kb_path = os.path.join(self.temp_dir, "data", "knowledge_base")
        os.makedirs(self.kb_path, exist_ok=True)
        
        # Create test document
        self.test_doc_content = "This is a test product document."
        with open(os.path.join(self.kb_path, "product_test.txt"), "w") as f:
            f.write(self.test_doc_content)

    def test_metadata_extraction(self):
        """Test metadata extraction from filename"""
        metadata = self.rag_tool._extract_metadata("product_test.txt", "content")
        self.assertEqual(metadata["type"], "product")

    def test_filter_matching(self):
        """Test document filter matching"""
        doc = {
            "metadata": {
                "type": "product",
                "category": "test"
            }
        }
        filters = {"type": "product"}
        self.assertTrue(self.rag_tool._matches_filters(doc, filters))

class TestKnowledgeAugmentationTool(unittest.TestCase):
    """Unit tests for the Knowledge Augmentation Tool"""
    
    def setUp(self):
        """Set up test environment"""
        self.tool = KnowledgeAugmentationTool()

    def test_execute_invalid_tool(self):
        """Test execution with invalid tool name"""
        result = self.tool.execute("invalid_tool", {})
        self.assertFalse(result["success"])
        self.assertIn("error_message", result)

    def test_execute_fetch_prospect_details(self):
        """Test execution of fetch_prospect_details"""
        result = self.tool.execute(
            "fetch_prospect_details",
            {"prospect_id": "123"}
        )
        self.assertIn("success", result)

if __name__ == '__main__':
    unittest.main() 