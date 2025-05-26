# Sailer AI - Intelligent Sales Assistant

Sailer AI is an advanced sales assistant system that helps sales representatives by providing real-time conversation analysis, context-aware responses, and intelligent tool integration. It combines the power of Large Language Models (LLM) with structured data sources to deliver accurate and helpful responses.

## Features

- 🤖 Real-time conversation analysis
- 📊 CRM data integration
- 📚 Knowledge base integration with RAG (Retrieval Augmented Generation)
- 🎯 Intent and entity recognition
- 💡 Smart response suggestions
- 📈 Performance monitoring

## System Requirements

- Python 3.9+
- Docker (optional)
- OpenAI API key

## Quick Start

### Option 1: Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Caua-Paduani/SailerAi_challenge.git
cd SailerAi_challenge
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4
DEBUG=false
```

5. Run the application:
```bash
uvicorn main:app --reload
```

### Option 2: Docker Setup

1. Build the Docker image:
```bash
docker build -t sailer-ai .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  --name sailer-ai-container \
  sailer-ai
```

## API Usage

The main endpoint is `/process_message`. Here's an example request:

```python
import requests
import json
from datetime import datetime

url = "http://localhost:8000/process_message"
data = {
    "conversation_history": [
        {
            "sender": "prospect",
            "content": "Hi, I'm interested in your products",
            "timestamp": datetime.now().isoformat()
        }
    ],
    "current_prospect_message": {
        "sender": "prospect",
        "content": "What's your pricing for enterprise customers?",
        "timestamp": datetime.now().isoformat()
    },
    "prospect_id": "123"
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

## Project Structure

```
SailerAi_challenge/
├── main.py           # FastAPI application
├── processor.py      # Core message processing
├── models.py         # Data models
├── tools.py          # Integration tools
├── llm.py           # LLM interaction
├── requirements.txt  # Dependencies
├── Dockerfile       # Docker configuration
└── data/            # Data directory
    ├── crm_data.json
    └── knowledge_base/
```

## Key Components

1. **Message Processing Pipeline**
   - Message analysis
   - Intent detection
   - Tool selection and execution
   - Response generation

2. **Knowledge Tools**
   - CRM integration for prospect data
   - RAG system for knowledge base access
   - Extensible tool framework

3. **LLM Integration**
   - OpenAI GPT models
   - Structured prompt engineering
   - Response synthesis

## Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test/
```

## Configuration

The system can be configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key | Required |
| MODEL | GPT model to use | gpt-4 |
| DEBUG | Enable debug mode | false |

## Data Requirements

1. **CRM Data**
   - Create `data/crm_data.json` with prospect information
   - Format: `{"prospect_id": {"name": "...", "email": "...", ...}}`

2. **Knowledge Base**
   - Add documents to `data/knowledge_base/`
   - Supported formats: `.txt` files
   - Organize by type (products, pricing, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Open an issue
3. Contact the maintainers

## Roadmap

- [ ] Add more knowledge tools
- [ ] Implement caching
- [ ] Add performance metrics
- [ ] Enhance response customization
- [ ] Add user feedback system
