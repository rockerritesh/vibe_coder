import os
import shutil
import glob
from typing import List
from .models import File

class FileManager:
    def create_readme(self, project_dir: str):
        """Create a README file with the project instructions."""
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(f"# Generated Project\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Instructions\n\n")
            f.write("1. Navigate to this directory\n")
            f.write("2. Install requirements: `pip install -r requirements.txt`\n")
            f.write("3. Run the application: See run_command.txt file\n")

    def create_files(self, project_dir: str, generated_code: List[File]) -> None:
        """Create files in the project directory based on generated code."""
        for file in generated_code:
            full_path = os.path.join(project_dir, file.name)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(file.content)

    def read_project_files(self, project_dir: str) -> list[File]:
        """Read all relevant files from a project directory."""
        files = []
        # Collect all Python files
        python_files = glob.glob(os.path.join(project_dir, "**/*.py"), recursive=True)
        # Add requirements.txt if it exists
        req_file = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_file):
            python_files.append(req_file)
        # Add any HTML templates
        template_files = glob.glob(os.path.join(project_dir, "**/*.html"), recursive=True)
        # Combine all files to read
        all_files = python_files + template_files
        for file_path in all_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    rel_path = os.path.relpath(file_path, project_dir)
                    files.append(File(name=rel_path, content=content))
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        return files

    def create_updated_project(self, event, selected_project: str) -> str:
        """Create a new version of the project directory with updates."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        updated_project_dir = f"{selected_project}_updated_{timestamp}"
        shutil.copytree(selected_project, updated_project_dir)
        self.create_files(updated_project_dir, event.generated_code)
        with open(os.path.join(updated_project_dir, "run_command.txt"), "w") as f:
            f.write(event.run_command)
        return updated_project_dir
