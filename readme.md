# Vibe Codder Agent

## Overview
The Vibe Codder Agent is designed for users who want to create projects with minimal or no coding. It leverages OpenAI's capabilities to assist in generating code and managing project environments.

## Features
- **No-Code Project Creation**: Generate projects without extensive coding knowledge.
- **Environment Management**: Create project-specific environments for debugging and running applications.
- **Code Generation**: Automatically generate code based on user requirements.
- **Project Analysis**: Analyze project structure and suggest updates.
- **Multi Model Support**: Till Now supported model are OPENAI, DEEPSEEK, LOCALLM, OLLAMA ETC.

## To-Do List
- [x] Add tools like read docs.
- [ ] Implement multiple language support.
- [ ] Create project-wise environment for debugging and running.
- [ ] Support additional models.

## Getting Started
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Navigate to the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Create.env file**: Copy `.envcopy` to `.env` (fill the env files)
4. **Update the `openai_client.py` for your suitable LLM.
4. **Run the Application**: Check the `run_command.txt` file for instructions on how to start the application.

## Project Structure
The generated project will include:
- `README.md`: Instructions for using the project.
- `requirements.txt`: List of dependencies.
- Source code files generated based on user input.

## Usage Instructions
- **Creating a Project**: Use the `create_project_directory()` function to set up a new project directory with a timestamp.
- **Generating Code**: Utilize the `get_event()` function to interact with OpenAI and generate code based on user requirements.
- **Running the Application**: Use the `run_application()` function to start the application and capture output/errors.

## Additional Information
- **Environment Variables**: Ensure that your OpenAI API key is set in your environment variables for the application to function correctly.
- **Project Management**: Use the `find_existing_projects()` function to list all previously generated projects.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please reach out to the project maintainer.

## old-version

On old_version directory.

## Limitation//Requirements
- Some times this miss to install requirements.txt
- Need Some KNowledge of Programming.

## Why Streamlit and Fastapi For Now
Streamlit and Fastapi is the best combo to make small app quickly.
