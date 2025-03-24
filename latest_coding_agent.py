from pydantic import BaseModel
from openai import OpenAI
import subprocess
import os
import shutil
import tempfile
from dotenv import load_dotenv
from datetime import datetime
import glob
import time

# Load environment variables
load_dotenv()

from openai_client import get_client
from models import File, RequirementsGatheringEvent, CodeGenerationEvent, ProjectAnalysisEvent
client = get_client()


def get_event(message: list, base_model: type) -> BaseModel:
    """Generate a response from OpenAI based on the conversation."""
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=message,
        response_format=base_model,
    )
    return completion.choices[0].message.parsed

def create_project_directory() -> str:
    """Create a unique project directory with timestamp and readable name."""
    # Get current timestamp for unique folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create user-friendly named directory in current directory
    base_dir = os.path.join(os.getcwd(), "generated_projects")
    os.makedirs(base_dir, exist_ok=True)
    
    # Create project directory with timestamp
    project_dir = os.path.join(base_dir, f"project_{timestamp}")
    os.makedirs(project_dir)
    
    # Create a README.md with instructions
    with open(os.path.join(project_dir, "README.md"), "w") as f:
        f.write(f"# Generated Project\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Instructions\n\n")
        f.write("1. Navigate to this directory\n")
        f.write("2. Install requirements: `pip install -r requirements.txt`\n")
        f.write("3. Run the application: See run_command.txt file\n")
    
    return project_dir

def create_files(project_dir: str, generated_code: list[File]) -> None:
    """Create files in the project directory based on generated code."""
    for file in generated_code:
        full_path = os.path.join(project_dir, file.name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(file.content)

def install_requirements(project_dir: str) -> bool:
    """Install dependencies if requirements.txt is present. Returns success status."""
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
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e.stderr}")
            return False
    return True  # Return True if no requirements file (nothing to install)

def get_application_url(run_command: str) -> str:
    """Determine the likely URL where the application will be available."""
    if "streamlit run" in run_command:
        return "http://localhost:8501"
    elif "uvicorn" in run_command:
        # Extract port if specified
        port = "8000"  # default
        if "--port" in run_command:
            parts = run_command.split()
            try:
                port_index = parts.index("--port") + 1
                if port_index < len(parts):
                    port = parts[port_index]
            except ValueError:
                pass
        return f"http://localhost:{port}/docs"  # FastAPI docs endpoint
    return "Unknown application URL"

def run_application(project_dir: str, run_command: str, timeout: int = 10) -> tuple[str | None, str | None]:
    """Run the application and capture output/errors with a configurable timeout."""
    try:
        process = subprocess.Popen(
            run_command.split(),
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output, error = process.communicate(timeout=timeout)
        return output, error
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"Process timed out after {timeout} seconds, but this may be normal for server applications.")
        output, error = process.communicate()
        # For web servers, timeout is expected behavior
        if "Streamlit" in run_command or "uvicorn" in run_command:
            return "Server started successfully (running in background)", None
        return output, error
    except Exception as e:
        return None, str(e)

def manage_application_process(project_dir: str, run_command: str) -> subprocess.Popen:
    """Start application in background and return process handle for later termination."""
    if os.name == 'nt':  # Windows
        process = subprocess.Popen(
            run_command.split(),
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:  # Unix/Linux/Mac
        process = subprocess.Popen(
            run_command.split(),
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
    return process

def find_existing_projects() -> list[str]:
    """Find all existing generated projects."""
    base_dir = os.path.join(os.getcwd(), "generated_projects")
    if not os.path.exists(base_dir):
        return []
    
    projects = glob.glob(os.path.join(base_dir, "project_*"))
    # Sort by creation time (newest first)
    return sorted(projects, key=os.path.getctime, reverse=True)

def get_project_info(project_dir: str) -> dict:
    """Get basic information about a project."""
    # Try to detect project type from run_command
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
    
    # Get creation time
    created_time = datetime.fromtimestamp(os.path.getctime(project_dir)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Get list of main files
    python_files = glob.glob(os.path.join(project_dir, "*.py"))
    python_files.extend(glob.glob(os.path.join(project_dir, "*/*.py")))
    main_files = [os.path.relpath(f, project_dir) for f in python_files[:5]]  # List up to 5 Python files
    
    return {
        "name": os.path.basename(project_dir),
        "path": project_dir,
        "type": project_type,
        "created": created_time,
        "run_command": run_command,
        "main_files": main_files
    }

def read_project_files(project_dir: str) -> list[File]:
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

def analyze_project(project_files: list[File]) -> dict:
    """Send project files to AI for analysis."""
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
    
    # Add each file as a separate message for context
    for file in project_files:
        message.append({
            "role": "user", 
            "content": f"File: {file.name}\n\n```python\n{file.content}\n```"
        })
    
    # Ask for structured analysis
    message.append({
        "role": "user", 
        "content": "Please provide a structured analysis of this project."
    })
    
    # Get analysis
    analysis = get_event(message, ProjectAnalysisEvent)
    return analysis

def main():
    print("=" * 80)
    print("Python Application Generator")
    print("=" * 80)
    
    # Check if user wants to create new project or update existing one
    print("Options:")
    print("1. Create a new Python application")
    print("2. Update an existing generated project")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "2":
        # Find existing projects
        projects = find_existing_projects()
        
        if not projects:
            print("No existing projects found. Creating a new project instead.")
            choice = "1"
        else:
            print("\nFound existing projects:")
            for i, project_path in enumerate(projects):
                info = get_project_info(project_path)
                print(f"{i+1}. {info['name']} - {info['type']} project (Created: {info['created']})")
                if info['main_files']:
                    print(f"   Main files: {', '.join(info['main_files'])}")
            
            # Let user select a project
            while True:
                try:
                    project_idx = int(input("\nSelect a project number to update (or 0 to create new): ")) - 1
                    if project_idx == -1:
                        choice = "1"
                        break
                    elif 0 <= project_idx < len(projects):
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a number.")
    
    if choice == "1":
        # Create a new project
        # Get initial user query
        query = input("What would you like to build today? (Streamlit app or FastAPI service): ")
        print("\nProject Description:", query)

        # Initialize conversation with more detailed system prompt
        message = [
            {
                "role": "system",
                "content": (
                    "You are a specialized programming assistant that creates Python applications using either Streamlit or FastAPI. "
                    "Follow this process:\n"
                    "1. Gather all requirements by asking targeted questions about functionality, features, and design.\n"
                    "2. Once you have sufficient information, generate all necessary code files.\n"
                    "3. Provide clear instructions for running the application.\n\n"
                    "Guidelines:\n"
                    "- Ask focused, specific questions to clarify the user's needs\n"
                    "- Include all necessary imports and dependencies\n"
                    "- For Streamlit: Create interactive, well-structured UI with appropriate widgets\n"
                    "- For FastAPI: Implement proper API endpoints with documentation, validation, and error handling\n"
                    "- Always include a requirements.txt file with all necessary dependencies\n"
                    "- Ensure code is robust, well-commented, and follows best practices"
                    "- Write requirements.txt without version name."
                ),
            },
            {"role": "user", "content": query},
        ]

        # Step 1: Gather requirements with progress feedback
        print("\n=== Gathering Requirements ===")
        link = input("Any Reference link eg doc: ")
        if len(link) > 0:
            # seperate link by space
            links = link.split()
            # run the subprocess to extract the text from the link `python scraper.py "https:sumityadav.com.np/biography"`
            for link in links:
                scraped_text = subprocess.run(["python", "scraper_doc.py", link], capture_output=True, text=True).stdout
                # add the link to the message
                print(f"Scraped text from {link}:\n{scraped_text}")
                # add the link to the message
                message.append({"role": "user", "content": f"Here is the reference link: {link} Docs \n{scraped_text}"})
        requirements_count = 0
        while True:
            event = get_event(message, RequirementsGatheringEvent)
            if event.all_details_gathered:
                print(f"\n✅ Requirements gathered ({requirements_count} questions answered)")
                print(f"\nProject Type: {event.project_type}")
                print(f"Requirements Summary:\n{event.requirements}")
                break
                
            requirements_count += 1
            print(f"\nQuestion {requirements_count}: {event.question}")
            user_response = input("Your response: ")
            message.append({"role": "assistant", "content": event.question})
            message.append({"role": "user", "content": user_response})
            

        # Step 2: Generate and refine code with improved feedback
        print("\n=== Generating and Running Code ===")
        max_attempts = 3
        final_project_dir = None
        
        for attempt in range(max_attempts):
            print(f"\nAttempt {attempt + 1}/{max_attempts}")
            
            # Generate code
            event = get_event(message, CodeGenerationEvent)
            file_list = [file.name for file in event.generated_code]
            print(f"Generated {len(file_list)} files: {', '.join(file_list)}")
            print("Run command:", event.run_command)

            # Create project directory and files
            project_dir = create_project_directory()
            create_files(project_dir, event.generated_code)
            
            # Save run command to file for reference
            with open(os.path.join(project_dir, "run_command.txt"), "w") as f:
                f.write(event.run_command)
            
            # Install requirements
            print("\nInstalling dependencies...")
            success = install_requirements(project_dir)
            if not success:
                print("⚠️ Failed to install dependencies, but attempting to run anyway")
            
            # Run the application with appropriate handling for web servers
            print("\nStarting application...")
            if "streamlit" in event.run_command.lower() or "uvicorn" in event.run_command.lower():
                # For web apps, we'll start in background and show URL
                try:
                    process = manage_application_process(project_dir, event.run_command)
                    # Wait briefly to catch immediate errors
                    time.sleep(2)
                    if process.poll() is not None:
                        # Process exited quickly - likely an error
                        _, error = process.communicate()
                        print(f"❌ Application failed to start: {error}")
                        # Add code and error to conversation for refinement
                        message.append({
                            "role": "assistant",
                            "content": f"I generated code but encountered an error when running it."
                        })
                        message.append({
                            "role": "user",
                            "content": f"Please refine the code to resolve this error: {error}"
                        })
                    else:
                        # Process is still running - likely success
                        app_url = get_application_url(event.run_command)
                        print(f"✅ Application started successfully!")
                        print(f"🌐 You can access it at: {app_url}")
                        print(f"📂 Project location: {project_dir}")
                        print(f"💻 To run it again: {event.run_command}")
                        final_project_dir = project_dir
                        process.terminate()  # Clean up the process
                        break
                except Exception as e:
                    print(f"❌ Error starting application: {str(e)}")
            else:
                # For non-web apps, run and capture output directly
                output, error = run_application(project_dir, event.run_command)
                if error:
                    print(f"❌ Error running application: {error}")
                    message.append({
                        "role": "assistant",
                        "content": f"I generated code but encountered an error when running it."
                    })
                    message.append({
                        "role": "user",
                        "content": f"Please refine the code to resolve this error: {error}"
                    })
                else:
                    print(f"✅ Application ran successfully!")
                    print(f"📂 Project location: {project_dir}")
                    print(f"💻 To run it again: {event.run_command}")
                    final_project_dir = project_dir
                    break
                    
            # Only clean up if we're continuing to another attempt
            if attempt < max_attempts - 1:
                shutil.rmtree(project_dir)
        
        # Final feedback
        if final_project_dir:
            print("\n=== Success! ===")
            print(f"Your application has been generated and is ready to use.")
            print(f"Location: {final_project_dir}")
        else:
            print(f"\n=== Unable to generate working code after {max_attempts} attempts ===")
            print("Please try again with a more specific description or simpler requirements.")
            
    else:  # Update existing project
        selected_project = projects[project_idx]
        project_info = get_project_info(selected_project)
        
        print(f"\n=== Analyzing Project: {project_info['name']} ===")
        print(f"Type: {project_info['type']}")
        print(f"Location: {project_info['path']}")
        
        # Read all project files
        project_files = read_project_files(selected_project)
        print(f"Reading {len(project_files)} files from project...")
        
        # Analyze project
        print("Analyzing project structure and features...")
        analysis = analyze_project(project_files)
        
        print("\n=== Project Analysis ===")
        print(f"Project Type: {analysis.project_type}")
        print(f"\nProject Structure:\n{analysis.project_structure}")
        print(f"\nMain Features:\n{analysis.main_features}")
        
        print("\nSuggested Updates:")
        for i, suggestion in enumerate(analysis.suggested_updates):
            print(f"{i+1}. {suggestion}")
            
        # Ask user what updates they want
        print("\n=== Update Requirements ===")
        update_query = input("What features or changes would you like to add to this project? ")
        
        # Initialize conversation with context of existing project
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
            {"role": "user", "content": f"I have an existing {analysis.project_type} project with the following structure and features:"},
            {"role": "user", "content": f"Project Structure:\n{analysis.project_structure}\n\nMain Features:\n{analysis.main_features}"},
        ]
        
        # Add each file as context
        for file in project_files:
            message.append({
                "role": "user", 
                "content": f"File: {file.name}\n\n```python\n{file.content}\n```"
            })
        
        # Add update request
        message.append({
            "role": "user", 
            "content": f"I want to update this project to: {update_query}"
        })
        
        # Generate updated code
        print("\n=== Generating Updates ===")
        event = get_event(message, CodeGenerationEvent)
        file_list = [file.name for file in event.generated_code]
        print(f"Generated/Updated {len(file_list)} files: {', '.join(file_list)}")
        print("Run command:", event.run_command)
        
        # Create a new version of the project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        updated_project_dir = f"{selected_project}_updated_{timestamp}"
        
        # Copy original project as base
        shutil.copytree(selected_project, updated_project_dir)
        
        # Apply updates (overwrite existing files and add new ones)
        create_files(updated_project_dir, event.generated_code)
        
        # Update run command if it changed
        with open(os.path.join(updated_project_dir, "run_command.txt"), "w") as f:
            f.write(event.run_command)
        
        # Install requirements
        print("\nInstalling dependencies...")
        success = install_requirements(updated_project_dir)
        if not success:
            print("⚠️ Failed to install dependencies, but attempting to run anyway")
        
        # Run the updated application
        print("\nStarting updated application...")
        if "streamlit" in event.run_command.lower() or "uvicorn" in event.run_command.lower():
            # For web apps, we'll start in background and show URL
            try:
                process = manage_application_process(updated_project_dir, event.run_command)
                # Wait briefly to catch immediate errors
                time.sleep(2)
                if process.poll() is not None:
                    # Process exited quickly - likely an error
                    _, error = process.communicate()
                    print(f"❌ Updated application failed to start: {error}")
                else:
                    # Process is still running - likely success
                    app_url = get_application_url(event.run_command)
                    print(f"✅ Updated application started successfully!")
                    print(f"🌐 You can access it at: {app_url}")
                    print(f"📂 Updated project location: {updated_project_dir}")
                    print(f"💻 To run it again: {event.run_command}")
                    process.terminate()  # Clean up the process
            except Exception as e:
                print(f"❌ Error starting updated application: {str(e)}")
        else:
            # For non-web apps, run and capture output directly
            output, error = run_application(updated_project_dir, event.run_command)
            if error:
                print(f"❌ Error running updated application: {error}")
            else:
                print(f"✅ Updated application ran successfully!")
                print(f"📂 Updated project location: {updated_project_dir}")
                print(f"💻 To run it again: {event.run_command}")
        
        print("\n=== Update Summary ===")
        print(f"Original project: {selected_project}")
        print(f"Updated project: {updated_project_dir}")
        print("Updated/Added files:")
        for file_name in file_list:
            print(f"- {file_name}")

if __name__ == "__main__":
    main()