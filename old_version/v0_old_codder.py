from pydantic import BaseModel
from openai import OpenAI
import subprocess
import os
import shutil
import tempfile
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model for individual files
class File(BaseModel):
    name: str
    content: str

# Model for gathering project requirements (unchanged)
class RequirementsGatheringEvent(BaseModel):
    all_details_gathered: bool
    question: str
    project_type: str  # "Streamlit" or "FastAPI"
    requirements: str  # Accumulated user requirements

# Model for code generation (updated)
class CodeGenerationEvent(BaseModel):
    generated_code: list[File]  # List of File objects
    run_command: str  # Command to run the application

def get_event(message: list, base_model: type) -> BaseModel:
    """Generate a response from OpenAI based on the conversation."""
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=message,
        response_format=base_model,
    )
    return completion.choices[0].message.parsed

# def create_project_directory() -> str:
#     """Create a unique temporary directory for the project."""
#     return tempfile.mkdtemp(prefix="project_")

def create_project_directory() -> str:
    """Create a unique project directory with timestamp."""
    # Get current timestamp for unique folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create base directory if it doesn't exist
    base_dir = os.path.join(os.getcwd(), "directory")
    os.makedirs(base_dir, exist_ok=True)
    
    # Create project directory with timestamp
    project_dir = os.path.join(base_dir, f"project_{timestamp}")
    os.makedirs(project_dir)
    
    return project_dir

def create_files(project_dir: str, generated_code: list[File]) -> None:
    """Create files in the project directory based on generated code."""
    for file in generated_code:
        full_path = os.path.join(project_dir, file.name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(file.content)

def install_requirements(project_dir: str) -> None:
    """Install dependencies if requirements.txt is present."""
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        try:
            subprocess.run(
                ["pip", "install", "-r", requirements_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e.stderr}")

def run_application(project_dir: str, run_command: str) -> tuple[str | None, str | None]:
    """Run the application and capture output/errors with a timeout."""
    try:
        process = subprocess.Popen(
            run_command.split(),
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output, error = process.communicate(timeout=10)
        return output, error
    except subprocess.TimeoutExpired:
        process.kill()
        output, error = process.communicate()
        return output, error
    except Exception as e:
        return None, str(e)

# grok code
def main():
    # Get initial user query
    query = input("Enter the project description (e.g., 'Create a Streamlit app to display Hello World'): ")
    print("Project Description:", query)

    # Initialize conversation
    message = [
        {
            "role": "system",
            "content": (
                "You are a programming assistant tasked with creating a Python application using Streamlit or FastAPI. "
                "First, gather all requirements by asking the user questions. Once all details are gathered, generate "
                "the code as a list of files, where each file has a 'name' (e.g., 'app.py', 'requirements.txt') and "
                "'content'. Also provide the run command (e.g., 'streamlit run app.py' or 'uvicorn main:app --reload')."
            ),
        },
        {"role": "user", "content": query},
    ]

    # Step 1: Gather requirements
    print("\n=== Gathering Requirements ===")
    while True:
        event = get_event(message, RequirementsGatheringEvent)
        if event.all_details_gathered:
            print("Requirements gathered:", event.requirements)
            break
        print(f"Assistant: {event.question}")
        user_response = input("Your response: ")
        message.append({"role": "user", "content": user_response})

    # Step 2: Generate and refine code
    print("\n=== Generating and Running Code ===")
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}")
        
        # Generate code
        event = get_event(message, CodeGenerationEvent)
        print("Generated files:", [file.name for file in event.generated_code])
        print("Run command:", event.run_command)

        # Create project directory and files
        project_dir = create_project_directory()
        create_files(project_dir, event.generated_code)
        
        # Install requirements
        install_requirements(project_dir)
        
        # Run the application
        output, error = run_application(project_dir, event.run_command)
        print("Output:", output or "None")
        if error:
            print("Error:", error)
            generated_code_str = "\n".join([f"{file.name}:\n{file.content}" for file in event.generated_code])
            message.append({
                "role": "assistant",
                "content": f"Generated code:\n{generated_code_str}\nRun command: {event.run_command}"
            })
            message.append({
                "role": "user",
                "content": f"Please refine the code to resolve this error: {error}"
            })
        else:
            print("Application ran successfully!")
            print("Instructions: Navigate to", project_dir, "and run:", event.run_command)
            break
        
        # Clean up after each attempt
        shutil.rmtree(project_dir)
    
    else:
        print(f"Failed to generate working code after {max_attempts} attempts.")
    
    # Final cleanup (if successful, keep the last directory for user access)
    if error and os.path.exists(project_dir):
        shutil.rmtree(project_dir)

if __name__ == "__main__":
    main()