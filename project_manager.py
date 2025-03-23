import os
import shutil
import subprocess
import glob
from datetime import datetime
from glob import glob
from .file_manager import FileManager
from .requirements_manager import RequirementsManager
from .application_executor import ApplicationExecutor
from .project_analyzer import ProjectAnalyzer
from .user_interaction import UserInteraction
from .openai_client import OpenAIClient

class ProjectManager:
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), "generated_projects")
        self.file_manager = FileManager()
        self.requirements_manager = RequirementsManager()
        self.app_executor = ApplicationExecutor()
        self.analyzer = ProjectAnalyzer()
        self.user_interface = UserInteraction()
        self.openai_client = OpenAIClient()

    def create_project_directory(self) -> str:
        """Create a unique project directory with timestamp and readable name."""
        # Get current timestamp for unique folder name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create user-friendly named directory in current directory
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Create project directory with timestamp
        project_dir = os.path.join(self.base_dir, f"project_{timestamp}")
        os.makedirs(project_dir)
        self.file_manager.create_readme(project_dir)
        return project_dir

    def find_existing_projects(self) -> list[str]:
        """Find all existing generated projects."""
        if not os.path.exists(self.base_dir):
            return []        
        projects = glob(os.path.join(self.base_dir, "project_*"))
        return sorted(projects, key=os.path.getctime, reverse=True)

    def get_project_info(self, project_dir: str) -> dict:
        """Get basic information about a project."""
        return self.analyzer.extract_project_info(project_dir)

    def manage_existing_project_updates(self, project_idx: int, projects: list):
        selected_project = projects[project_idx]
        project_info = self.get_project_info(selected_project)
        
        print(f"\n=== Analyzing Project: {project_info['name']} ===")
        print(f"Type: {project_info['type']}")
        print(f"Location: {project_info['path']}")
        
        # Read all project files
        project_files = self.file_manager.read_project_files(selected_project)
        print(f"Reading {len(project_files)} files from project...")
        
        # Analyze project
        print("Analyzing project structure and features...")
        analysis = self.analyzer.analyze_project(project_files)
        print("\n=== Project Analysis ===")
        print(f"Project Type: {analysis['project_type']}")
        print(f"\nProject Structure:\n{analysis['project_structure']}")
        print(f"\nMain Features:\n{analysis['main_features']}")        
        print("\nSuggested Updates:")
        for i, suggestion in enumerate(analysis['suggested_updates']):
            print(f"{i+1}. {suggestion}")
        
        # Ask user what updates they want
        print("\n=== Update Requirements ===")
        update_query = input("What features or changes would you like to add to this project? ")
        
        # Initialize conversation with context of existing project
        message = self.analyzer.create_update_conversation(analysis, project_files, update_query)
        
        # Generate updated code
        print("\n=== Generating Updates ===")
        event = self.openai_client.get_event(message)
        updated_project_dir = self.file_manager.create_updated_project(event, selected_project)

        # Run the updated application
        self.app_executor.execute_application(updated_project_dir, event.run_command)