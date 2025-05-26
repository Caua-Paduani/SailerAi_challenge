import pytest
import os
import tempfile
import json
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def test_app():
    """Create a test FastAPI client"""
    return TestClient(app)

@pytest.fixture(scope="function")
def test_data_dir():
    """Create temporary test data directories"""
    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "data", "knowledge_base"), exist_ok=True)
    
    yield temp_dir
    
    # Cleanup after tests
    import shutil
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def crm_test_data(test_data_dir):
    """Create test CRM data"""
    crm_data = {
        "123": {
            "name": "Test Prospect",
            "email": "test@example.com",
            "company": "Test Corp",
            "status": "Lead"
        }
    }
    
    crm_file = os.path.join(test_data_dir, "data", "crm_data.json")
    with open(crm_file, "w") as f:
        json.dump(crm_data, f)
    
    return crm_data

@pytest.fixture(scope="function")
def knowledge_base_test_data(test_data_dir):
    """Create test knowledge base documents"""
    kb_content = {
        "product_info.txt": """
        Product: Test Product
        Description: This is a test product with amazing features.
        Price: $100/month
        Features:
        - Feature 1
        - Feature 2
        """,
        "pricing.txt": """
        Basic Plan: $50/month
        Pro Plan: $100/month
        Enterprise: Custom pricing
        """,
        "objections.txt": """
        Common objection: Price too high
        Response: Focus on value and ROI
        """
    }
    
    for filename, content in kb_content.items():
        file_path = os.path.join(test_data_dir, "data", "knowledge_base", filename)
        with open(file_path, "w") as f:
            f.write(content)
    
    return kb_content 