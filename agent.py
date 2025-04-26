from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent # Added LoopAgent
from google.adk.tools import google_search as GoogleSearchTool
from google.adk.tools import built_in_code_execution as CodeExecutionTool
from google.adk.tools import agent_tool

# Shared state for storing approval flags
shared_state = {
    "frontend_approved": False,
    "backend_approved": False,
    "task_completed": False
}

# 1. Define the individual role agents:

product_manager = LlmAgent(
    name="ProductManager",
    model="gemini-2.0-flash",
    description="Acts as a Product Manager to gather and clarify requirements.",
instruction=open("o3agent/product_manager_instruction.txt", "r").read(),
    tools=[GoogleSearchTool],
    # Assume ADK can prompt user via an interaction – this could be a loop or tool to get user input.
    output_key="requirements"  # save the refined requirements in shared state
)

# Tech Lead - Instructions will be updated to handle both design and review
tech_lead = LlmAgent(
    name="TechLead",
    model="gemini-2.0-flash",
    description="Tech Lead who designs architecture OR reviews submitted code.", # Updated description
instruction=open("o3agent/tech_lead_instruction.txt", "r").read(), # Instructions file will be updated
    tools=[GoogleSearchTool],
    # Output keys will be managed by updated instructions (e.g., architecture_design, frontend_review_feedback, backend_review_feedback, frontend_approved, backend_approved)
)

# Frontend Developer - Instructions will be updated to generate code and handle feedback
frontend_dev = LlmAgent(
    name="FrontendDev",
    model="gemini-2.0-flash",
    description="Frontend Developer who implements the Blazor WASM interface based on design and feedback.", # Updated description
instruction=open("o3agent/frontend_dev_instruction.txt", "r").read(), # Instructions file will be updated
    tools=[GoogleSearchTool], # Potentially add CodeExecutionTool if needed for snippets
    output_key="frontend_code" # Will output code to this key
    # Will read feedback from keys like 'frontend_review_feedback' based on updated instructions
    post_process=lambda output: shared_state.update({"frontend_approved": True}) # Updates shared_state flag upon task completion
)

# Backend Developer - Instructions will be updated to generate code and handle feedback
backend_dev = LlmAgent(
    name="BackendDev",
    model="gemini-2.0-flash",
    description="Backend Developer who implements Azure Functions API logic based on design and feedback.", # Updated description
instruction=open("o3agent/backend_dev_instruction.txt", "r").read(), # Instructions file will be updated
    tools=[GoogleSearchTool], # Potentially add CodeExecutionTool
    output_key="backend_code" # Will output code to this key
    # Will read feedback from keys like 'backend_review_feedback' based on updated instructions
    post_process=lambda output: shared_state.update({"backend_approved": True}) # Updates shared_state flag upon task completion
)

db_engineer = LlmAgent(
    name="DBEngineer",
    model="gemini-2.0-flash",
    description="Database Engineer who configures the Cosmos DB database.",
instruction=open("o3agent/db_engineer_instruction.txt", "r").read(),
    tools=[GoogleSearchTool], # Added GoogleSearchTool
    output_key="db_schema"
    # (Potentially could use a tool to actually create a schema or validate with Azure APIs, but omitted in this local simulation.)
)

qa_engineer = LlmAgent(
    name="QAEngineer",
    model="gemini-2.0-flash",
    description="QA Engineer who tests the application thoroughly.",
instruction=open("o3agent/qa_engineer_instruction.txt", "r").read(),
    tools=[CodeExecutionTool, GoogleSearchTool],  # Added GoogleSearchTool
    output_key="test_report"
)

consolidation_agent = LlmAgent(
    name="ConsolidationAgent",
    model="gemini-2.0-flash",
    description="Consolidates outputs from all agents.",
instruction=open("o3agent/consolidation_agent_instruction.txt", "r").read(),
    output_key="final_output"
)

# 2. Orchestrate the agents in a workflow:

# Define the development and review loop
# Note: The TechLead agent's instructions MUST be updated to check state
# (e.g., 'component_under_review') to know whether to review frontend or backend code.
# State needs to be set appropriately before calling TechLead each time.
# For simplicity here, we assume the updated TechLead instruction handles this context switching.
# A more complex implementation might involve separate 'ReviewFrontend' and 'ReviewBackend' agents
# or agents that explicitly set the 'component_under_review' state before calling the TechLead.

development_review_loop = LoopAgent(
    name="DevelopmentReviewLoop",
    sub_agents=[
        frontend_dev,       # Frontend dev implements/revises based on state
        tech_lead,          # Tech lead reviews frontend code (needs state context)
        backend_dev,        # Backend dev implements/revises based on state
        tech_lead           # Tech lead reviews backend code (needs state context)
        # A loop controller agent could be added here to check approval status and signal termination
    ],
    max_iterations=3 # Limit iterations to prevent infinite loops
    # Termination logic needs to be handled by updated TechLead instructions setting approval flags
    # and potentially a final check agent or logic within the loop/consolidation agent.
)

# Create the main sequential orchestrator agent
root_agent = SequentialAgent(
    name="DevTeamOrchestrator",
    sub_agents=[
        product_manager,
        tech_lead,                 # Initial architecture design phase
        development_review_loop,   # Development and review loop
        db_engineer,
        qa_engineer,
        consolidation_agent
    ]
)

# 3. Running the orchestration (example usage):
#user_request = "I want to create a task tracking app that allows users to add, complete, and share tasks."
#result = dev_team_orchestrator.run(input=user_request)

#print(result["test_report"])  # The final test report after QA (or collect all outputs from state as needed)
