# o3agent Directory

This directory contains the implementation of an AI agent system, with different agents specializing in various roles within a software development lifecycle.

## File Structure

```
o3agent/
├── __init__.py
├── .env
├── agent.py
├── backend_dev_instruction.txt
├── consolidation_agent_instruction.txt
├── db_engineer_instruction.txt
├── frontend_dev_instruction.txt
├── product_manager_instruction.txt
├── qa_engineer_instruction.txt
└── tech_lead_instruction.txt
```

## File Descriptions

*   `__init__.py`: This file initializes the o3agent module, making it importable.
*   `.env`: Create a .env filve file contains environment variables used by the agents, such as API keys or configuration settings.
*   `agent.py`: This file likely contains the main agent class and logic for running the agents.
*   `backend_dev_instruction.txt`: This file contains instructions for the Backend Developer AI agent, specifying its role, objective, and task.
*   `consolidation_agent_instruction.txt`: This file contains instructions for the Consolidation Agent AI, which collects and summarizes outputs from other agents.
*   `db_engineer_instruction.txt`: This file contains instructions for the Database Engineer AI, responsible for designing the database schema.
*   `frontend_dev_instruction.txt`: This file contains instructions for the Frontend Developer AI agent, specifying its role, objective, and task.
*   `product_manager_instruction.txt`: This file contains instructions for the Product Manager AI agent, responsible for gathering requirements and defining the product vision.
*   `qa_engineer_instruction.txt`: This file contains instructions for the QA Engineer AI agent, responsible for generating test cases and verifying the app's functionality.
*   `tech_lead_instruction.txt`: This file contains instructions for the Tech Lead AI agent, responsible for designing the system architecture and reviewing code.
