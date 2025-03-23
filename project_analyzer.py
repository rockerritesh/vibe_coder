from typing import List
from .models import File

class ProjectAnalyzer:
    def extract_project_info(self, project_dir: str) -> dict:
        run_command_path = os.path.join(project_dir, "run_command.txt")
        project_type = "Unknown"
        run_command = ""

        if os.path.exists(run_command_path):
            with open(run_command_path, "r") as f:
                run_command = f.read().strip()
                if "streamlit" in run_command.lower():
                    project_type = "Streamlit"
                elif "uvicorn" in run_command.lower() or "fastapi" in run_command.lower():
                    project_type = "FastAPI"

        created_time = datetime.fromtimestamp(os.path.getctime(project_dir)).strftime("%Y-%m-%d %H:%M:%S")

        python_files = glob.glob(os.path.join(project_dir, "*.py"))
        python_files.extend(glob.glob(os.path.join(project_dir, "*/*.py")))
        main_files = [os.path.relpath(f, project_dir) for f in python_files[:5]]

        return {
            "name": os.path.basename(project_dir),
            "path": project_dir,
            "type": project_type,
            "created": created_time,
            "run_command": run_command,
            "main_files": main_files
        }

    def analyze_project(self, project_files: List[File]) -> dict:
        message = [
            {
                "role": "system",
                "content": (
                    "You are a Python application analyzer. Examine the provided code files "
                    "and provide a comprehensive analysis of the project. Identify the key features, "
                    "structure, and possible areas for enhancement. Be specific and technical. "
                    "Focus on understanding what the app does, how it works, and what could be improved or added."
                ),
            },
            {
                "role": "user", 
                "content": "Here are the files from a Python project. Please analyze them:"
            }
        ]

        for file in project_files:
            message.append({
                "role": "user", 
                "content": f"File: {file.name}\n\n```python\n{file.content}\n```"
            })

        message.append({
            "role": "user", 
            "content": "Please provide a structured analysis of this project."
        })

        analysis = self.get_event(message)
        return analysis

    def create_update_conversation(self, analysis, project_files, update_query):
        message = [
            {
                "role": "system",
                "content": (
                    "You are a specialized programming assistant that updates existing Python applications. "
                    "You will be provided with the existing code files and the user's update requirements. "
                    "Your task is to generate updated versions of files or new files as needed. "
                    "Make sure your updates integrate well with the existing codebase and follow the same style and patterns. "
                    "Always include all necessary imports and dependencies. "
                    "If you modify the requirements.txt file, include all original dependencies plus any new ones."
                ),
            },
            {"role": "user", "content": f"I have an existing {analysis['project_type']} project with the following structure and features:"},
            {"role": "user", "content": f"Project Structure:\n{analysis['project_structure']}\n\nMain Features:\n{analysis['main_features']}"},
        ]
        for file in project_files:
            message.append({
                "role": "user", 
                "content": f"File: {file.name}\n\n```python\n{file.content}\n```"
            })
        message.append({
            "role": "user", 
            "content": f"I want to update this project to: {update_query}"
        })
        return message
