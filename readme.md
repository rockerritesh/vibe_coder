# Vibe Codder Agent

## Overview
The Vibe Codder Agent is designed for users who want to create projects with minimal or no coding. It leverages OpenAI's capabilities to assist in generating code and managing project environments.

## Features
- **No-Code Project Creation**: Generate projects without extensive coding knowledge.
- **Environment Management**: Create project-specific environments for debugging and running applications.
- **Code Generation**: Automatically generate code based on user requirements.
- **Project Analysis**: Analyze project structure and suggest updates.
- **Multi Model Support**: Till Now supported model are OPENAI, DEEPSEEK, LOCALLM, OLLAMA ETC.

## Example
```
`python latest_coding_agent.py`
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project

Enter your choice (1 or 2): 1
What would you like to build today? (Streamlit app or FastAPI service): streamlti

Project Description: streamlit

=== Gathering Requirements ===
Any Reference link eg doc: 

Question 1: What kind of application do you want to build with Streamlit? For example, a data visualization app, a form submission app, or something else?
Your response: fluid visualization with mouse movment

Question 2: What type of fluid visualization are you looking to create? Is it a simulation of fluid dynamics, interactive visualizations using data, or something else? Additionally, what kind of data or input will drive the visualization?
Your response: yes

Question 3: Could you specify the type of data or parameters you want to use for the fluid dynamics simulation? Also, do you want users to be able to manipulate the simulation parameters in real-time using UI elements?
Your response: all

✅ Requirements gathered (3 questions answered)

Project Type: Streamlit
Requirements Summary:
- Create a fluid dynamics visualization simulation using Streamlit.
- Allow users to interact with the simulation via mouse movement.
- Provide real-time parameter adjustment capabilities through UI elements.
- Ensure the application handles various input data types for the simulation.

=== Generating and Running Code ===

Attempt 1/3
Generated 2 files: app.py, requirements.txt
Run command: streamlit run app.py

Installing dependencies...
Dependencies installed successfully.

Starting application...
✅ Application started successfully!
🌐 You can access it at: http://localhost:8501
📂 Project location: ../generated_projects/project_20250325_074450
💻 To run it again: streamlit run app.py

=== Success! ===
Your application has been generated and is ready to use.
Location: /run/media/limsim/extra/AGENT-CODE-SUPPORT/generated_projects/project_20250325_074450
```

## To-Do List
- [x] Add tools like read docs.
- [ ] Multiple LLM call for creation of multiple files.
- [ ] Wirite unit test(Fastapi).
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

## Demo
![alt text](image.png)

