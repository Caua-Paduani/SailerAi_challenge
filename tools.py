from typing import Dict, Optional, List
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import faiss

class KnowledgeAugmentationTool:
    """A multi-purpose tool that can fetch information from different sources."""

    def __init__(self):
        self.crm_tool = CRMtool()# for CRM data
        self.rag_tool = RAGtool() #knowledge base


#execute the fetch_prospect_details tool or query_knowledge_base tool if needed
    def execute(self, tool_name:str, tool_params:Dict) -> Dict:
        try:
            if tool_name == "fetch_prospect_details":
                result = self.crm_tool.fetch_prospect_details(tool_params.get("prospect_id"))
            elif tool_name == "query_knowledge_base":
                result = self.rag_tool.query_knowledge_base(tool_params.get("query"), tool_params.get("filters"))
            else:
                return{
                    "success":False,
                    "error_message":f"Tool {tool_name} not found"
                }
            return{
                "tool_name":tool_name,
                "input_parameters": tool_params,   
                "output_result": result,           
                "success": True,                   
                "error_message": None 
            }
        except Exception as e:
            return{
                "success":False,
                "error_message":str(e)
            }

#CRM tool        
class CRMtool:
    """Tool for interacting with the CRM system."""
#load CRM data 
    def __init__(self):
        self.crm_data = self.load_crm_data()
        #fetch details from CRM
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
    #function to load CRM data from JSON file
    def load_crm_data(self) -> Dict:
        """Load CRM data from JSON file"""
        crm_data_path = "data/crm_data.json"
        try:
            #load the CRM data from the JSON file as read only
            with open(crm_data_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"error": "CRM data file not found"}
        

class RAGtool:
    """Tool for interacting with the knowledge base."""

    def __init__(self):
        #load the model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = self.load_documents()
        self.index = self.create_index()
    def query_knowledge_base(self,query:str, filters: Optional[Dict] = None):
        """Search the knowledge base for imformations matching the query"""
        if not query:
            return {"error": "Query is required"}
        #convert query to vector
        query_embedding = self.model.encode([query])
        k = 3
        #search for the k most similar documents
        D,I = self.index.search(np.array([query_embedding],dtype=np.float32),k)
        results = []
        for i, idx in enumerate(I[0]):
            if idx != -1 and idx < len(self.documents):
                doc = self.documents[idx]
                
                # apply  filters if provided
                if filters and not self._matches_filters(doc, filters):
                    continue
                
                results.append({
                    "content": doc["content"],
                    "source": doc["filename"],
                    "metadata": doc["metadata"],
                    "relevance_score": float(D[0][i])
                })
        return {
            "results": results,
            "query": query,
            "filters_applied": filters is not None
        }

    def _matches_filters(self, doc:Dict, filters:Dict) -> bool:
        """Check if the document matches the filters"""
        for key, value in filters.items():
            if key not in doc["metadata"] or doc["metadata"][key] != value:
                return False
        return True
            
    def _extract_metadata(self, filename: str, content: str) -> Dict:
        """Extract metadata from document filename and content"""
        metadata = {}
        
        # Extract document type based on filename
        if "product" in filename.lower():
            metadata["type"] = "product"
        elif "pricing" in filename.lower():
            metadata["type"] = "pricing"
        elif "objection" in filename.lower():
            metadata["type"] = "sales_playbook"
        else:
            metadata["type"] = "general"
        
        return metadata

    def load_documents(self):
        # load documents from the knowledge base
        kb_path = "data/knowledge_base"
        documents = []
        if not os.path.exists(kb_path):
            os.makedirs(kb_path,exist_ok=True)
            print(f"Directory {kb_path} created, please add some documents...")
            return documents
        #verify if there are any .txt files in the knowledge base
        txt_files = [f for f in os.listdir(kb_path) if f.endswith(".txt")]
        if not txt_files:
            print(f"No .txt documents found in {kb_path}")
            return documents
        
        for file in txt_files:
            file_path = os.path.join(kb_path,file)
        try:
            #load the content of the file
            with open(file_path, 'r') as file:
                content = file.read()
                #extract metadata from the file 
                metadata = self._extract_metadata(file, content)
                documents.append({
                    "filename":file,
                    "content":content,
                    "metadata":metadata
                })
                print(f"Loaded document {file} with metadata: {metadata}")
        except Exception as e:
            print(f"Error loading document {file}: {e}")
            return documents

    def create_index(self):
        # create a FAISS index for semantic search
        if not self.documents:
            print("No documents to index")
            dimension = 384 
            return faiss.IndexFlatL2(dimension)
        
        #generate embeddings for all documents
        texts = [doc["content"] for doc in self.documents]
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        
        #create a FAISS index
        index = faiss.IndexFlatL2(dimension)
        #add the embeddings to the index
        index.add(np.array(embeddings).astype("float32"))
        print(f"Created index with {len(texts)} documents")
        return index
    
   