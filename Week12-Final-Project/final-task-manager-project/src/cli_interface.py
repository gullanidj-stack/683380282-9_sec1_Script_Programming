"""Command-line interface. Contains no business logic; delegates to TaskManager."""
import datetime


class CLIInterface:
    def __init__(self, task_manager):
        self.manager = task_manager

    # --- Input helpers ---
    def display_menu(self):
        print("\n--- Enhanced Task Manager Menu ---")
        print("1. Add Normal Task")
        print("2. Add Due Date Task")
        print("3. Add Priority Task")
        print("4. List All Tasks")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
        print("0. Exit")
        print("----------------------------------")

    def get_user_choice(self):
        return input("Enter your choice (0-9): ").strip()

    def get_task_description(self):
        while True:
            description = input("Enter task description: ").strip()
            if description:
                return description
            print("Task description cannot be empty. Please try again.")

    def get_due_date_input(self):
        while True:
            s = input("Enter due date (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(s, "%Y-%m-%d")
                return s
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-12-31).")

    def get_priority_input(self):
        while True:
            p = input("Enter priority (High/Medium/Low): ").strip().capitalize()
            if p in ["High", "Medium", "Low"]:
                return p
            print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")

    @staticmethod
    def _parse_tags(text):
        return [t.strip().lower() for t in text.split(",") if t.strip()]

    def get_tags_input(self):
        return self._parse_tags(
            input("Enter tags (comma-separated, e.g., work,urgent - optional): "))

    @staticmethod
    def _optional_date(prompt, label):
        s = input(prompt).strip()
        if not s:
            return None
        try:
            return datetime.datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print(f"Invalid '{label}' format. Ignoring.")
            return None

    @staticmethod
    def _ask_task_id(action):
        try:
            return int(input(f"Enter ID of task to {action}: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number for Task ID.")
            return None

    def _display_tasks(self, tasks, title="Tasks"):
        if not tasks:
            print(f"No {title.lower()} found.")
            return
        print(f"\n--- {title} ---")
        for task in tasks:
            print(task)
        print("------------------")

    # --- Menu actions ---
    def _handle_filter(self):
        print("\n--- Filter Tasks ---")
        s = input("Filter by completed status (yes/no, blank for all): ").strip().lower()
        status = True if s == "yes" else False if s == "no" else None
        before = self._optional_date(
            "Filter by due date before (YYYY-MM-DD, blank for all): ", "due date before")
        after = self._optional_date(
            "Filter by due date after (YYYY-MM-DD, blank for all): ", "due date after")
        p = input("Filter by priority (High/Medium/Low, blank for all): ").strip().capitalize()
        priority = p if p in ["High", "Medium", "Low"] else None
        tags = self._parse_tags(input(
            "Filter by tags (comma-separated, must have ALL, blank for all): ")) or None
        result = self.manager.filter_tasks(status=status, due_date_before=before,
                                           due_date_after=after, priority_level=priority,
                                           contains_tags=tags)
        self._display_tasks(result, "Filtered Tasks")

    def _handle_sort(self):
        print("\n--- Sort Tasks ---")
        print("Available criteria: id, description, completed, due_date, priority")
        criterion = input("Sort by (default: id): ").strip().lower() or "id"
        reverse = input("Reverse order (yes/no, default: no): ").strip().lower() == "yes"
        order = "(Descending)" if reverse else "(Ascending)"
        self._display_tasks(self.manager.sort_tasks(criterion, reverse),
                            f"Sorted Tasks by {criterion} {order}")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                desc = self.get_task_description()
                t = self.manager.add_normal_task(desc, tags=self.get_tags_input())
                print(f"Normal Task '{t.description}' added with ID {t.id}.")
            elif choice == "2":
                desc = self.get_task_description()
                due = self.get_due_date_input()
                t = self.manager.add_due_date_task(desc, due, tags=self.get_tags_input())
                if t:
                    print(f"Due Date Task '{t.description}' (Due: "
                          f"{t.due_date.strftime('%Y-%m-%d')}) added with ID {t.id}.")
                else:
                    print("Failed to add Due Date Task. Please check your input.")
            elif choice == "3":
                desc = self.get_task_description()
                pr = self.get_priority_input()
                t = self.manager.add_priority_task(desc, pr, tags=self.get_tags_input())
                if t:
                    print(f"Priority Task '{t.description}' (Priority: {t.priority}) "
                          f"added with ID {t.id}.")
                else:
                    print("Failed to add Priority Task. Please check your input.")
            elif choice == "4":
                self._display_tasks(self.manager.get_all_tasks(), "Your Tasks")
            elif choice == "5":
                tid = self._ask_task_id("complete")
                if tid is not None:
                    print(self.manager.complete_task(tid)[1])
            elif choice == "6":
                tid = self._ask_task_id("delete")
                if tid is not None:
                    print(self.manager.delete_task(tid)[1])
            elif choice == "7":
                kw = input("Enter search keyword (in description or tags): ").strip()
                self._display_tasks(self.manager.search_tasks(kw), f"Search Results for '{kw}'")
            elif choice == "8":
                self._handle_filter()
            elif choice == "9":
                self._handle_sort()
            elif choice == "0":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 9.")
