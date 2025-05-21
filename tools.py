from typing import Dict
import json
class KnowledgeAugmentationTool:
    """A multi-purpose tool that can fetch information from different sources."""

    def __init__(self):
        self.crm_tool = CRMtool()# for CRM data
        self.rag_tool = RAGtool() #knowledge base
#CRM tool        
class CRMtool:
    """Tool for interacting with the CRM system."""

    def __init__(self):
        self.crm_data = self.load_crm_data()
    def fetch_prospect_details(self, prospect_id:str) -> Dict:
        """Fetch prospect details from CRM"""
        if not prospect_id:
            return {"error": "Prospect ID is required"}
        if prospect_id in self.crm_data:
            return {
            "prospect_found":True,
            "prospect_details":self.crm_data[prospect_id]
        }
        else:
            return {
                "prospect_found":False,
                "error":f"Prospect with ID {prospect_id} not found"
            }
    #load CRM data from JSON file
    def load_crm_data(self) -> Dict:
        """Load CRM data from JSON file"""
        crm_data_path = "data/crm_data.json"
        try:
            with open(crm_data_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"error": "CRM data file not found"}
        
#RAG tool
class RAGtool:
    """Tool for interacting with the knowledge base."""

    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        
        

    
  