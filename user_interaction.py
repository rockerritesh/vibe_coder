class UserInteraction:
    @staticmethod
    def choose_option() -> str:
        print("Options:")
        print("1. Create a new Python application")
        print("2. Update an existing generated project")
        choice = input("\nEnter your choice (1 or 2): ").strip()
        return choice

    @staticmethod
    def get_initial_query() -> str:
        query = input("What would you like to build today? (Streamlit app or FastAPI service): ")
        print("\nProject Description:", query)
        return query

    @staticmethod
    def get_requirements_response(question: str, count: int) -> str:
        print(f"\nQuestion {count}: {question}")
        return input("Your response: ")

    @staticmethod
    def select_project(projects: list) -> int:
        print("\nFound existing projects:")
        for i, project_path in enumerate(projects):
            print(f"{i+1}. {project_path}")
        while True:
            try:
                selection = int(input("\nSelect a project number to update (or 0 to create new): ")) - 1
                if selection == -1 or 0 <= selection < len(projects):
                    return selection
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a number.")

    @staticmethod
    def summarize_success(final_project_dir: str):
        print("\n=== Success! ===")
        print(f"Your application has been generated and is ready to use.")
        print(f"Location: {final_project_dir}")

    @staticmethod
    def summarize_failure(max_attempts: int):
        print(f"\n=== Unable to generate working code after {max_attempts} attempts ===")
        print("Please try again with a more specific description or simpler requirements.")
