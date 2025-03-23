import os
import subprocess

class RequirementsManager:
    def install_requirements(self, project_dir: str) -> bool:
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
