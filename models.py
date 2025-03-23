from pydantic import BaseModel

class File(BaseModel):
    name: str
    content: str

class RequirementsGatheringEvent(BaseModel):
    all_details_gathered: bool
    question: str
    project_type: str  # "Streamlit" or "FastAPI"
    requirements: str  # Accumulated user requirements

class CodeGenerationEvent(BaseModel):
    generated_code: list[File]  # List of File objects
    run_command: str  # Command to run the application

class ProjectAnalysisEvent(BaseModel):
    project_structure: str  # Description of project structure and key files
    project_type: str  # "Streamlit" or "FastAPI"
    main_features: str  # Summary of main features
    suggested_updates: list[str]  # Suggested potential updates
