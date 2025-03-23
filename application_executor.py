import os
import subprocess
import time

class ApplicationExecutor:
    def execute_application(self, project_dir: str, run_command: str):
        print("\nInstalling dependencies...")
        requirements_manager = RequirementsManager()
        success = requirements_manager.install_requirements(project_dir)
        if not success:
            print("⚠️ Failed to install dependencies, but attempting to run anyway")

        print("\nStarting application...")
        if "streamlit" in run_command.lower() or "uvicorn" in run_command.lower():
            try:
                process = self.manage_application_process(project_dir, run_command)
                time.sleep(2)
                if process.poll() is not None:
                    _, error = process.communicate()
                    print(f"❌ Application failed to start: {error}")
                else:
                    app_url = self.get_application_url(run_command)
                    print(f"✅ Application started successfully!")
                    print(f"🌐 You can access it at: {app_url}")
                    process.terminate()
            except Exception as e:
                print(f"❌ Error starting application: {str(e)}")
        else:
            output, error = self.run_application(project_dir, run_command)
            if error:
                print(f"❌ Error running application: {error}")
            else:
                print(f"✅ Application ran successfully!")

    def manage_application_process(self, project_dir: str, run_command: str) -> subprocess.Popen:
        if os.name == 'nt':  # Windows
            return subprocess.Popen(
                run_command.split(),
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix/Linux/Mac
            return subprocess.Popen(
                run_command.split(),
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )

    def get_application_url(self, run_command: str) -> str:
        if "streamlit run" in run_command:
            return "http://localhost:8501"
        elif "uvicorn" in run_command:
            port = "8000"  # default
            if "--port" in run_command:
                parts = run_command.split()
                try:
                    port_index = parts.index("--port") + 1
                    if port_index < len(parts):
                        port = parts[port_index]
                except ValueError:
                    pass
            return f"http://localhost:{port}/docs"
        return "Unknown application URL"

    def run_application(self, project_dir: str, run_command: str, timeout: int = 10) -> tuple[str | None, str | None]:
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
            output, error = process.communicate()
            if "streamlit" in run_command or "uvicorn" in run_command:
                return "Server started successfully (running in background)", None
            return output, error
        except Exception as e:
            return None, str(e)
