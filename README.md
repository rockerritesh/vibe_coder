# Vibe Coder Agent

An AI-powered code generation tool that creates Python applications and HTML websites with minimal coding knowledge required. Leverages multiple LLM providers to assist in generating, managing, and executing projects through an interactive CLI interface.

## Overview

The Vibe Coder Agent is designed for users who want to create projects with minimal or no coding experience. It uses artificial intelligence to automatically generate code, manage project environments, and handle dependency installation. The tool supports creating Streamlit applications, FastAPI services, and static HTML websites through conversational AI-driven requirements gathering.

## Features

- **🚀 No-Code Project Creation**: Generate complete applications without extensive coding knowledge
- **🤖 AI-Powered Requirements Gathering**: Interactive conversation to understand your project needs
- **📁 Environment Management**: Create project-specific environments with timestamped directories
- **⚡ Automatic Code Generation**: Generate complete applications based on user requirements
- **🔄 Project Analysis & Updates**: Analyze existing projects and suggest improvements
- **🌐 Multi-Platform Support**: Create Streamlit apps, FastAPI services, and HTML websites
- **🔧 Multiple LLM Support**: Compatible with OpenAI, DeepSeek, Local LLM, and Ollama
- **📦 Dependency Management**: Automatic installation and management of project dependencies
- **🏃 Application Execution**: Built-in support for running and testing generated applications

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- API access to at least one supported LLM provider

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/vibe_coder.git
   cd vibe_coder
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .envcopy .env
   ```
   
   Edit the `.env` file with your API keys and configuration:
   ```bash
   nano .env  # or use your preferred editor
   ```

4. **Update LLM Client Configuration**
   
   The `openai_client.py` file handles LLM provider connections. For most providers, you only need to update the `.env` file, but for custom setups, you may need to modify this file:
   
   ```python
   # openai_client.py - Default configuration
   from openai import OpenAI
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   def get_client():
       client = OpenAI(
           api_key=os.getenv("OPENAI_API_KEY"), 
           base_url=os.getenv("BASE_URL_OPENAI")
       )
       return client
   ```
   
   For different providers, update the environment variables in `.env` accordingly.

5. **Verify Installation**
   
   Test your setup by running:
   ```bash
   python latest_coding_agent.py
   ```
   
   You should see the main menu with three options. If you encounter errors, check the troubleshooting section below.

### Complete Setup Example (OpenAI)

Here's a complete setup example using OpenAI:

```bash
# 1. Clone and navigate
git clone https://github.com/your-username/vibe_coder.git
cd vibe_coder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .envcopy .env

# 4. Edit .env file (replace with your actual API key)
echo 'OPENAI_API_KEY=sk-proj-your-actual-openai-key-here' > .env
echo 'BASE_URL_OPENAI=https://api.openai.com/v1/' >> .env
echo 'MODEL_NAME=gpt-3.5-turbo' >> .env

# 5. Test the setup
python latest_coding_agent.py
```

### Virtual Environment Setup (Recommended)

For better dependency management, use a virtual environment:

```bash
# Create virtual environment
python -m venv vibe_coder_env

# Activate virtual environment
# On Windows:
vibe_coder_env\Scripts\activate
# On macOS/Linux:
source vibe_coder_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Continue with setup...
```

## Configuration

### Environment Variables

The application uses the following environment variables (defined in `.env`). These variables are based on the template provided in `.envcopy`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here
BASE_URL_OPENAI=https://api.openai.com/v1/

# DeepSeek Configuration  
BASE_URL_DEEPSEEK=https://api.deepseek.com/v1/

# Local LLM Configuration
LOCAL_URL=http://127.0.0.1:1234
LOCAL_API_KEY=your-local-api-key

# Model Configuration
MODEL_NAME=qwen2.5-coder-3b-instruct
```

**Key Environment Variables:**
- **`OPENAI_API_KEY`**: Your API key for the selected LLM provider
- **`BASE_URL_OPENAI`**: The base URL for API requests (changes based on provider)
- **`MODEL_NAME`**: The specific model to use for code generation
- **`LOCAL_URL`**: Base URL for local LLM servers (Local LLM/Ollama)
- **`LOCAL_API_KEY`**: API key for local servers (if required)

### Supported LLM Providers

#### OpenAI Configuration
- **Supported Models**: 
  - `gpt-3.5-turbo` (recommended for cost-effectiveness)
  - `gpt-4` (higher quality, more expensive)
  - `gpt-4-turbo` (latest GPT-4 variant)
  - `gpt-4o` (optimized version)
- **Setup Steps**: 
  1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
  2. Set in `.env`: `OPENAI_API_KEY=sk-proj-your-actual-key`
  3. Set base URL: `BASE_URL_OPENAI=https://api.openai.com/v1/`
  4. Choose model: `MODEL_NAME=gpt-3.5-turbo` or `gpt-4`
- **Example Configuration**:
  ```bash
  OPENAI_API_KEY=sk-proj-abc123def456ghi789
  BASE_URL_OPENAI=https://api.openai.com/v1/
  MODEL_NAME=gpt-3.5-turbo
  ```

#### DeepSeek Configuration
- **Supported Models**: 
  - `deepseek-coder` (specialized for code generation)
  - `deepseek-chat` (general conversation and coding)
  - `deepseek-coder-6.7b-instruct` (specific model variant)
- **Setup Steps**:
  1. Get API key from [DeepSeek Platform](https://platform.deepseek.com/)
  2. Set in `.env`: `OPENAI_API_KEY=your-deepseek-key`
  3. Set base URL: `BASE_URL_OPENAI=https://api.deepseek.com/v1/`
  4. Choose model: `MODEL_NAME=deepseek-coder` or `deepseek-chat`
- **Example Configuration**:
  ```bash
  OPENAI_API_KEY=sk-deepseek-abc123def456
  BASE_URL_OPENAI=https://api.deepseek.com/v1/
  MODEL_NAME=deepseek-coder
  ```

#### Local LLM Configuration
- **Supported Platforms**: 
  - LM Studio (recommended for beginners)
  - text-generation-webui (advanced users)
  - vLLM server
  - FastChat server
  - Any OpenAI-compatible local server
- **Common Models**:
  - `qwen2.5-coder-3b-instruct` (lightweight, good for coding)
  - `codellama-7b-instruct` (Meta's code-focused model)
  - `deepseek-coder-6.7b-instruct` (local version)
  - `mistral-7b-instruct` (general purpose)
- **Setup Steps**:
  1. Install and start your local LLM server (e.g., LM Studio on port 1234)
  2. Load your preferred model in the server
  3. Set in `.env`: `OPENAI_API_KEY=not-needed` (placeholder)
  4. Set base URL: `BASE_URL_OPENAI=http://127.0.0.1:1234/v1/`
  5. Set model name: `MODEL_NAME=your-loaded-model-name`
- **Example Configuration**:
  ```bash
  OPENAI_API_KEY=local-placeholder
  BASE_URL_OPENAI=http://127.0.0.1:1234/v1/
  MODEL_NAME=qwen2.5-coder-3b-instruct
  ```

#### Ollama Configuration
- **Supported Models**: 
  - `qwen2.5-coder:3b` (lightweight coding model)
  - `qwen2.5-coder:7b` (better performance, larger size)
  - `codellama:7b` (Meta's CodeLlama model)
  - `deepseek-coder:6.7b` (DeepSeek's coding model)
  - `mistral:7b` (general purpose model)
  - `llama3:8b` (Meta's latest model)
- **Setup Steps**:
  1. Install Ollama from [ollama.ai](https://ollama.ai/)
  2. Start Ollama service: `ollama serve`
  3. Pull desired model: `ollama pull qwen2.5-coder:3b`
  4. Verify model: `ollama list`
  5. Set in `.env`: `OPENAI_API_KEY=ollama` (placeholder)
  6. Set base URL: `BASE_URL_OPENAI=http://localhost:11434/v1/`
  7. Set model: `MODEL_NAME=qwen2.5-coder:3b`
- **Example Configuration**:
  ```bash
  OPENAI_API_KEY=ollama-placeholder
  BASE_URL_OPENAI=http://localhost:11434/v1/
  MODEL_NAME=qwen2.5-coder:3b
  ```
- **Alternative Port Configuration**:
  ```bash
  # If Ollama runs on different port
  BASE_URL_OPENAI=http://localhost:11434/v1/
  # Or for remote Ollama instance
  BASE_URL_OPENAI=http://your-server-ip:11434/v1/
  ```

### Configuration Tips and Best Practices

#### Choosing the Right Provider
- **OpenAI**: Best for production use, highest quality output, requires paid API access
- **DeepSeek**: Good balance of cost and performance, specialized coding models
- **Local LLM**: Complete privacy, no API costs, requires local hardware resources
- **Ollama**: Easy local setup, good for development and testing, free to use

#### Model Selection Guidelines
- **For Code Generation**: Use coding-specialized models like `deepseek-coder`, `qwen2.5-coder`, or `codellama`
- **For General Tasks**: Use chat models like `gpt-3.5-turbo`, `deepseek-chat`, or `mistral`
- **For Resource Constraints**: Use smaller models like `qwen2.5-coder:3b` or `mistral:7b`
- **For Best Quality**: Use larger models like `gpt-4`, `qwen2.5-coder:7b`, or `codellama:13b`

#### Environment Variable Reference
Based on the `.envcopy` template, here are all available configuration options:

```bash
# Primary API Configuration
OPENAI_API_KEY=your-api-key-here          # Required for all providers
BASE_URL_OPENAI=provider-base-url         # Provider-specific base URL
MODEL_NAME=model-name                     # Model to use for generation

# Alternative URLs (from .envcopy)
BASE_URL_DEEPSEEK=https://api.deepseek.com/v1/
LOCAL_URL=http://127.0.0.1:1234          # Local LLM server URL
LOCAL_API_KEY=your-local-api-key         # Local server API key (if needed)
```

#### Provider Switching
To switch between providers, simply update these three variables in your `.env` file:
```bash
# Switch to DeepSeek
OPENAI_API_KEY=your-deepseek-key
BASE_URL_OPENAI=https://api.deepseek.com/v1/
MODEL_NAME=deepseek-coder

# Switch to Local LLM
OPENAI_API_KEY=local-placeholder
BASE_URL_OPENAI=http://127.0.0.1:1234/v1/
MODEL_NAME=qwen2.5-coder-3b-instruct

# Switch to Ollama
OPENAI_API_KEY=ollama-placeholder
BASE_URL_OPENAI=http://localhost:11434/v1/
MODEL_NAME=qwen2.5-coder:3b
```

## Usage

### Quick Start

Run the application:
```bash
python latest_coding_agent.py
```

### Main Options

The application provides three main options:

1. **Create a new Python application** - Generate Streamlit apps or FastAPI services
2. **Update an existing generated project** - Modify and enhance previously created projects  
3. **Create a static HTML website** - Generate complete HTML/CSS/JavaScript websites

### Example Workflow

```
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project
3. Create a static HTML website

Enter your choice (1, 2 or 3): 1
What would you like to build today? (Streamlit app or FastAPI service): streamlit app

Project Description: streamlit app

=== Gathering Requirements ===
Any Reference link eg doc: 

Question 1: What kind of application do you want to build with Streamlit?
Your response: data visualization dashboard

Question 2: What type of data will you be visualizing?
Your response: sales data with charts and graphs

✅ Requirements gathered (2 questions answered)

=== Generating and Running Code ===
Generated 3 files: app.py, requirements.txt, README.md
✅ Application started successfully!
🌐 You can access it at: http://localhost:8501
📂 Project location: /path/to/generated_projects/project_20250107_143022
```

## Project Structure

```
vibe_coder/
├── latest_coding_agent.py      # Main application entry point
├── models.py                   # Pydantic models for structured AI responses
├── openai_client.py           # LLM client configuration
├── application_executor.py    # Application execution handler
├── project_analyzer.py        # Project analysis functionality
├── project_manager.py         # Project creation and management
├── file_manager.py            # File operations utilities
├── requirements_manager.py    # Dependency management
├── user_interaction.py        # User interface components
├── scraper_doc.py            # Web scraping for reference docs
├── utils.py                  # General utilities
├── requirements.txt          # Project dependencies
├── .envcopy                 # Environment variables template
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md              # This file
├── run_command.txt        # Execution instructions
├── generated_projects/    # Directory for generated projects
└── old_version/          # Previous versions
    ├── v0.1_latest_coding_agent.py
    └── v0_old_coder.py
```

### Key Files Description

#### Core Application Files

- **`latest_coding_agent.py`** (Main Entry Point - 687 lines)
  - Contains the main application logic and CLI interface
  - Handles user interaction flow for all three main features
  - Manages the conversation flow with AI for requirements gathering
  - Orchestrates code generation, project creation, and application execution
  - Implements the main menu system and user choice handling
  - Contains functions for project directory creation and file management

- **`models.py`** (Pydantic Models)
  - Defines structured data models for AI responses using Pydantic
  - `File`: Model for individual code files (name, content)
  - `RequirementsGatheringEvent`: Model for AI requirements gathering responses
  - `CodeGenerationEvent`: Model for AI code generation responses with file lists
  - `ProjectAnalysisEvent`: Model for project analysis and update suggestions
  - Ensures type safety and structured communication with LLM APIs

- **`openai_client.py`** (LLM Client Configuration)
  - Handles LLM provider connections and client initialization
  - Configures OpenAI-compatible clients for different providers
  - Manages API key and base URL configuration from environment variables
  - Provides unified interface for all supported LLM providers
  - Contains the `get_client()` function used throughout the application

#### Project Management Components

- **`application_executor.py`** (Application Execution Handler)
  - Manages running and testing of generated applications
  - Handles dependency installation via requirements.txt
  - Starts web applications (Streamlit/FastAPI) and manages processes
  - Provides application URL detection and status reporting
  - Implements error handling for application startup failures
  - Supports both web applications and command-line tools

- **`project_analyzer.py`** (Project Analysis Functionality)
  - Analyzes existing projects for structure and content
  - Extracts project information including type, creation date, and main files
  - Provides project metadata for the update functionality
  - Identifies project types (Streamlit, FastAPI, HTML) from run commands
  - Supports project listing and selection for updates

- **`project_manager.py`** (Project Creation and Management)
  - Handles project directory creation with timestamp-based naming
  - Manages project organization in the `generated_projects` folder
  - Coordinates between different components for project lifecycle
  - Provides project discovery and listing functionality
  - Integrates file management, requirements management, and execution

- **`file_manager.py`** (File Operations Utilities)
  - Handles file creation, reading, and writing operations
  - Manages project file structure creation
  - Provides utilities for file system operations
  - Handles file encoding and error management
  - Supports batch file operations for project generation

- **`requirements_manager.py`** (Dependency Management)
  - Manages Python package dependencies and requirements.txt files
  - Handles automatic dependency installation using pip
  - Provides error handling for dependency installation failures
  - Supports virtual environment detection and management
  - Implements retry logic for failed installations

#### User Interface and Utilities

- **`user_interaction.py`** (User Interface Components)
  - Handles CLI user interface elements and prompts
  - Manages user input validation and processing
  - Provides consistent formatting for user messages
  - Implements interactive question-answer flows
  - Handles user choice validation and error messages

- **`scraper_doc.py`** (Web Scraping for Reference Documentation)
  - Extracts content from reference URLs provided by users
  - Processes web pages to extract relevant text content
  - Integrates scraped content into AI conversation context
  - Supports multiple URL processing for comprehensive documentation
  - Handles web scraping errors and content formatting

- **`utils.py`** (General Utilities)
  - Contains shared utility functions used across the application
  - Provides common helper functions for string processing, file operations
  - Implements logging and debugging utilities
  - Contains constants and configuration helpers

#### Configuration and Documentation Files

- **`requirements.txt`** (Project Dependencies)
  - Lists all Python packages required for the application
  - Includes core dependencies: fastapi, openai, pydantic, streamlit, uvicorn
  - Used for automatic dependency installation during setup
  - Pinned versions ensure consistent behavior across environments

- **`.envcopy`** (Environment Variables Template)
  - Template file containing all supported environment variables
  - Includes configuration for OpenAI, DeepSeek, Local LLM, and Ollama
  - Contains BASE_URL configurations and model name examples
  - Users copy this to `.env` and fill in their actual API keys

- **`.gitignore`** (Git Ignore Rules)
  - Excludes sensitive files like `.env` from version control
  - Ignores Python cache files, virtual environments
  - Excludes generated projects directory from repository
  - Maintains clean repository structure

- **`LICENSE`** (MIT License)
  - MIT License terms for the project
  - Copyright information and usage permissions
  - Legal framework for open-source distribution

- **`run_command.txt`** (Execution Instructions)
  - Simple text file containing the main execution command
  - Contains: `python3 latest_coding_agent.py`
  - Quick reference for running the application

#### Directory Structure

- **`generated_projects/`** (Generated Projects Directory)
  - Contains all AI-generated projects with timestamp-based naming
  - Each project has format: `project_YYYYMMDD_HHMMSS`
  - Automatically created when first project is generated
  - Projects include source code, requirements.txt, and run commands

- **`old_version/`** (Previous Versions)
  - Contains earlier versions of the application for reference
  - `v0.1_latest_coding_agent.py`: Previous version of main application
  - `v0_old_coder.py`: Original version of the coding agent
  - Maintained for backward compatibility and development history

### Generated Project Structure

When the application creates a new project, it generates the following structure:

```
generated_projects/project_20250107_143022/
├── app.py                    # Main application file (Streamlit/FastAPI)
├── requirements.txt          # Project-specific dependencies
├── README.md                # Project documentation
├── run_command.txt          # Command to run the application
├── static/                  # Static files (for web projects)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/               # HTML templates (for FastAPI projects)
    └── index.html
```

#### Generated Project File Types

- **Streamlit Projects**: Generate `app.py` with Streamlit components and UI elements
- **FastAPI Projects**: Generate `main.py` with API endpoints, models, and documentation
- **HTML Projects**: Generate `index.html`, CSS files, and JavaScript for static websites
- **Common Files**: All projects include `requirements.txt`, `README.md`, and `run_command.txt`

## Usage Examples and Workflows

### Feature 1: Creating New Python Applications

#### Example 1: Streamlit Data Visualization Dashboard

**Complete User Interaction Flow:**

```bash
$ python latest_coding_agent.py
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project
3. Create a static HTML website

Enter your choice (1, 2 or 3): 1
What would you like to build today? (Streamlit app or FastAPI service): streamlit dashboard

Project Description: streamlit dashboard

=== Gathering Requirements ===
Any Reference link eg doc: 

Question 1: What kind of data visualization dashboard do you want to create? What type of data will it display?
Your response: sales analytics dashboard with charts showing revenue trends, product performance, and customer demographics

Question 2: What specific chart types would you like to include? (e.g., line charts, bar charts, pie charts, scatter plots)
Your response: line charts for revenue trends, bar charts for product sales, pie charts for customer segments, and interactive filters

Question 3: Do you want the dashboard to use sample data or connect to a specific data source?
Your response: use sample sales data with realistic numbers

✅ Requirements gathered (3 questions answered)

=== Generating and Running Code ===
Attempt 1/3
Generated 4 files: app.py, requirements.txt, README.md, sample_data.py
Run command: streamlit run app.py

Installing dependencies...
✅ Dependencies installed successfully

Starting application...
✅ Application started successfully!
🌐 You can access it at: http://localhost:8501
📂 Project location: /path/to/generated_projects/project_20250107_143022
💻 To run it again: streamlit run app.py

=== Success! ===
Your application has been generated and is ready to use.
Location: /path/to/generated_projects/project_20250107_143022
```

**Generated Files:**
- `app.py`: Main Streamlit application with interactive dashboard
- `requirements.txt`: Dependencies (streamlit, pandas, plotly, numpy)
- `README.md`: Project documentation and usage instructions
- `sample_data.py`: Sample sales data generator

#### Example 2: FastAPI REST API Service

**Complete User Interaction Flow:**

```bash
$ python latest_coding_agent.py
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project
3. Create a static HTML website

Enter your choice (1, 2 or 3): 1
What would you like to build today? (Streamlit app or FastAPI service): fastapi todo api

Project Description: fastapi todo api

=== Gathering Requirements ===
Any Reference link eg doc: 

Question 1: What kind of API endpoints do you want for your todo application?
Your response: CRUD operations - create, read, update, delete todos, plus list all todos and mark as complete

Question 2: What data fields should each todo item have?
Your response: id, title, description, completed status, created date, due date, priority level

Question 3: Do you want authentication, database integration, or just in-memory storage for now?
Your response: in-memory storage with Pydantic models, no authentication needed for now

✅ Requirements gathered (3 questions answered)

=== Generating and Running Code ===
Attempt 1/3
Generated 5 files: main.py, models.py, requirements.txt, README.md, test_api.py
Run command: uvicorn main:app --reload

Installing dependencies...
✅ Dependencies installed successfully

Starting application...
✅ Application started successfully!
🌐 You can access it at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
📂 Project location: /path/to/generated_projects/project_20250107_144530
💻 To run it again: uvicorn main:app --reload

=== Success! ===
Your application has been generated and is ready to use.
Location: /path/to/generated_projects/project_20250107_144530
```

**Generated Files:**
- `main.py`: FastAPI application with CRUD endpoints
- `models.py`: Pydantic models for Todo items
- `requirements.txt`: Dependencies (fastapi, uvicorn, pydantic)
- `README.md`: API documentation and usage examples
- `test_api.py`: Sample API test requests

### Feature 2: Updating Existing Projects

**Complete User Interaction Flow:**

```bash
$ python latest_coding_agent.py
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project
3. Create a static HTML website

Enter your choice (1, 2 or 3): 2

Found existing projects:
1. project_20250107_143022 - Streamlit project (Created: 2025-01-07 14:30:22)
   Main files: app.py, sample_data.py
2. project_20250107_144530 - FastAPI project (Created: 2025-01-07 14:45:30)
   Main files: main.py, models.py

Select a project number to update (or 0 to create new): 1

Selected project: /path/to/generated_projects/project_20250107_143022

=== Analyzing Project ===
Project Type: Streamlit
Main Features: Sales analytics dashboard with revenue trends, product performance charts, and customer demographics visualization
Current Files: app.py, sample_data.py, requirements.txt, README.md

What updates would you like to make to this project?
Your input: add user authentication and the ability to upload custom CSV data files

=== Gathering Update Requirements ===
Question 1: What type of authentication do you want to implement? (simple password, user accounts, OAuth, etc.)
Your response: simple password protection with a login form

Question 2: What CSV file format should users be able to upload? What columns are expected?
Your response: CSV files with columns: date, product, revenue, customer_segment, region

Question 3: Should the uploaded data replace the sample data or be added alongside it?
Your response: replace the sample data and allow users to switch between different uploaded datasets

✅ Update requirements gathered (3 questions answered)

=== Generating Updated Code ===
Generated 6 files: app.py, auth.py, data_handler.py, requirements.txt, README.md, sample_data.py
Updated/Added files:
- app.py (enhanced with authentication and file upload)
- auth.py (new - authentication functions)
- data_handler.py (new - CSV processing)
- requirements.txt (updated with new dependencies)

✅ Updated application started successfully!
🌐 You can access it at: http://localhost:8501
📂 Updated project location: /path/to/generated_projects/project_20250107_143022_updated_20250107_150015

=== Update Summary ===
Original project: /path/to/generated_projects/project_20250107_143022
Updated project: /path/to/generated_projects/project_20250107_143022_updated_20250107_150015
Updated/Added files:
- app.py
- auth.py
- data_handler.py
- requirements.txt
```

### Feature 3: Creating HTML Websites

**Complete User Interaction Flow:**

```bash
$ python latest_coding_agent.py
================================================================================
Python Application Generator
================================================================================
Options:
1. Create a new Python application
2. Update an existing generated project
3. Create a static HTML website

Enter your choice (1, 2 or 3): 3
What kind of website would you like to build? portfolio website for a web developer

Website Description: portfolio website for a web developer

=== Gathering Requirements ===
Any Reference link eg doc: 

Question 1: What sections do you want on your portfolio website?
Your response: header with navigation, about me section, skills showcase, project portfolio with images, contact form, and footer

Question 2: What color scheme and design style do you prefer?
Your response: modern dark theme with blue accents, clean minimalist design, responsive layout

Question 3: Do you want any interactive features or animations?
Your response: smooth scrolling, hover effects on project cards, animated skill bars, and a working contact form

✅ Requirements gathered (3 questions answered)

=== Generating and Running Code ===
Attempt 1/3
Generated 8 files: index.html, styles.css, script.js, images/placeholder.jpg, README.md, contact.php, projects.json, favicon.ico
Run command: python -m http.server 8000

Starting application...
✅ Application started successfully!
🌐 You can access it at: http://localhost:8000
📂 Project location: /path/to/generated_projects/project_20250107_151245
💻 To run it again: python -m http.server 8000

=== Success! ===
Your application has been generated and is ready to use.
Location: /path/to/generated_projects/project_20250107_151245
```

**Generated Files:**
- `index.html`: Main HTML structure with all sections
- `styles.css`: Complete CSS with dark theme and responsive design
- `script.js`: JavaScript for animations and interactivity
- `contact.php`: Backend script for contact form processing
- `projects.json`: Sample project data
- `images/`: Directory with placeholder images
- `README.md`: Website documentation and deployment instructions

### Sample Inputs and Expected Outputs

#### Input Examples for Different Project Types

**Streamlit Applications:**
- "data analysis tool for CSV files"
- "machine learning model comparison dashboard"
- "financial calculator with charts"
- "image processing application"
- "real-time data monitoring dashboard"

**FastAPI Services:**
- "user management API with authentication"
- "file upload and processing service"
- "data analytics API with database"
- "notification system with webhooks"
- "inventory management REST API"

**HTML Websites:**
- "business landing page with contact form"
- "photography portfolio with gallery"
- "restaurant website with menu and reservations"
- "personal blog with article management"
- "e-commerce product showcase"

#### Expected Output Structure

**For Streamlit Projects:**
```
generated_projects/project_YYYYMMDD_HHMMSS/
├── app.py                 # Main Streamlit application
├── requirements.txt       # streamlit, pandas, plotly, etc.
├── README.md             # Usage instructions
├── run_command.txt       # streamlit run app.py
└── data/                 # Sample data files (if needed)
    └── sample_data.csv
```

**For FastAPI Projects:**
```
generated_projects/project_YYYYMMDD_HHMMSS/
├── main.py               # FastAPI application
├── models.py             # Pydantic models
├── requirements.txt      # fastapi, uvicorn, pydantic
├── README.md            # API documentation
├── run_command.txt      # uvicorn main:app --reload
└── tests/               # API tests (if generated)
    └── test_main.py
```

**For HTML Projects:**
```
generated_projects/project_YYYYMMDD_HHMMSS/
├── index.html           # Main HTML file
├── styles.css           # CSS styling
├── script.js            # JavaScript functionality
├── README.md           # Deployment instructions
├── run_command.txt     # python -m http.server 8000
├── images/             # Image assets
│   └── placeholder.jpg
└── assets/             # Additional assets
    ├── fonts/
    └── icons/
```

### CLI Interface Navigation

**Main Menu Options:**
1. **Option 1**: Create new Python application → Choose Streamlit or FastAPI → Requirements gathering → Code generation
2. **Option 2**: Update existing project → Select from list → Describe changes → Enhanced code generation
3. **Option 3**: Create HTML website → Describe website type → Requirements gathering → Static site generation

**Requirements Gathering Process:**
- AI asks 2-5 targeted questions based on project type
- User provides detailed responses for better code generation
- Optional reference documentation URLs can be provided
- Process continues until AI has sufficient information

**Code Generation and Execution:**
- Up to 3 attempts to generate working code
- Automatic dependency installation
- Application startup and URL provision
- Error handling and retry logic
- Success confirmation with project location

## Troubleshooting

### Common Issues

**Dependency Installation Failures**
- Ensure you have Python 3.8+ installed
- Try upgrading pip: `pip install --upgrade pip`
- Use virtual environment to avoid conflicts

**API Key Configuration Problems**
- Verify your API keys are correctly set in `.env`
- Check that the BASE_URL matches your provider
- Ensure your API key has sufficient credits/permissions

**Model Compatibility Issues**
- Verify the MODEL_NAME in `.env` matches your provider's available models
- Some models may not support structured output - try different models
- Check provider documentation for supported features

**Application Won't Start**
- Check if required ports (8501 for Streamlit, 8000 for FastAPI) are available
- Verify all dependencies are installed correctly
- Check the generated `run_command.txt` for specific instructions

## Limitations

- **Dependency Installation**: Occasionally fails to install requirements.txt automatically
- **Programming Knowledge**: Some basic programming understanding helpful for troubleshooting
- **Model Limitations**: Generated code quality depends on the chosen LLM model
- **Complex Applications**: Better suited for small to medium-sized applications
- **Internet Connection**: Required for API-based LLM providers

## Architecture Overview

```
User Input → Requirements Gathering → AI Code Generation → Project Creation → Dependency Installation → Application Execution

┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   CLI       │    │ Requirements │    │    LLM      │    │   Project    │
│ Interface   │───▶│  Gathering   │───▶│  Generation │───▶│  Creation    │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                           │                                       │
                           ▼                                       ▼
                   ┌──────────────┐                      ┌──────────────┐
                   │   Document   │                      │ Dependency   │
                   │   Scraping   │                      │ Management   │
                   └──────────────┘                      └──────────────┘
                                                                 │
                                                                 ▼
                                                        ┌──────────────┐
                                                        │ Application  │
                                                        │  Execution   │
                                                        └──────────────┘
```

## Why Streamlit and FastAPI?

Streamlit and FastAPI provide the best combination for rapid application development:

- **Streamlit**: Perfect for data visualization, dashboards, and interactive web apps
- **FastAPI**: Excellent for REST APIs, microservices, and backend development
- **Quick Development**: Both frameworks enable rapid prototyping and deployment
- **Python Ecosystem**: Leverage the rich Python ecosystem for data science and web development

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the project maintainer
- Check existing documentation and troubleshooting guides

---

**Demo Screenshots**

### FastAPI Application
![FastAPI Demo](image.png)

### HTML Website  
![HTML Demo](image-1.png)













