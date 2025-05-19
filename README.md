# Sailer AI – Autonomous Sales Agent

This project implements a simplified version of an autonomous AI Sales Agent. Its purpose is to handle individual conversation turns with sales prospects by performing the following:

- **Contextual Message Processing:** Analyzes incoming prospect messages within the context of the conversation history.
- **LLM-Orchestrated Reasoning:** Uses a large language model to understand intent, extract entities, determine sentiment, and decide next steps.
- **Tool Integration:** Dynamically decides whether external information is needed and invokes tools like:
  - CRM data retrieval
  - Knowledge base search (using a RAG pipeline)
- **Response Generation:** Synthesizes a structured output that includes:
  - A draft response to the prospect
  - Internal recommended actions
  - A tool usage log
  - A confidence score
  - (Optionally) Reasoning trace for transparency
- **Evaluation Framework:** Includes offline evaluation with a golden dataset, automated metrics for intent/entity accuracy, and strategies for prompt testing and monitoring.

The project demonstrates advanced LLM interaction, structured reasoning, and modular backend design using clean architecture principles.
