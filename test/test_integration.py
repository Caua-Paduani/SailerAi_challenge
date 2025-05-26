import unittest
from fastapi.testclient import TestClient
from datetime import datetime
import json
import os
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
        # Criar diretórios necessários
        os.makedirs("data/knowledge_base", exist_ok=True)
        
        # Criar dados de teste do CRM
        self.crm_data = {
            "123": {
                "name": "Test Prospect",
                "email": "test@example.com",
                "company": "Test Corp"
            }
        }
        with open("data/crm_data.json", "w") as f:
            json.dump(self.crm_data, f)
        
        # Criar documento de teste da base de conhecimento
        self.kb_content = """
        Product: Test Product
        Price: $100/month
        Features: Feature 1, Feature 2
        """
        with open("data/knowledge_base/product.txt", "w") as f:
            f.write(self.kb_content)

    def test_process_message(self):
        """Teste básico do endpoint process_message"""
        request_data = {
            "conversation_history": [
                {
                    "sender": "prospect",
                    "content": "Hi",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "current_prospect_message": {
                "sender": "prospect",
                "content": "What are your product features?",
                "timestamp": datetime.now().isoformat()
            },
            "prospect_id": "123"
        }
        
        response = self.client.post("/process_message", json=request_data)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("actionable_insights", data)
        self.assertIn("suggested_reply", data)
        self.assertIsInstance(data["next_steps"], list)

    def test_error_handling(self):
        """Teste de tratamento de erro com dados inválidos"""
        invalid_request = {
            "conversation_history": [],
            "current_prospect_message": {
                "sender": "prospect",
                "content": "",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        response = self.client.post("/process_message", json=invalid_request)
        self.assertEqual(response.status_code, 422)  # Erro de validação

    def tearDown(self):
        """Limpar arquivos de teste"""
        if os.path.exists("data/crm_data.json"):
            os.remove("data/crm_data.json")
        if os.path.exists("data/knowledge_base/product.txt"):
            os.remove("data/knowledge_base/product.txt")

if __name__ == '__main__':
    unittest.main() 