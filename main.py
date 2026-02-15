import ctypes
import subprocess
import sys
import shlex

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    """Relaunches the script with administrator privileges."""
    if not is_admin():
        print("Administrator privileges required. Elevating...")
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        try:
            subprocess.run(['powershell', 'Start-Process', sys.executable, '-ArgumentList', params, '-Verb', 'runAs'], check=True)
        except subprocess.CalledProcessError:
            print("Failed to elevate privileges. Please run as administrator.")
        sys.exit(0)

class WinMan:
    """A utility class for managing Windows local user accounts and groups."""

    @staticmethod
    def execute(command):
        """Executes a given command and handles errors."""
        try:
            run = subprocess.run(command, check=True, capture_output=True, text=True)
            if run.stdout:
                print(run.stdout)
            if run.stderr:
                print(run.stderr)
            return run
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with return code {e.returncode}")
            print(f"Command: {' '.join(e.cmd)}")
            if e.stderr:
                print(f"Error output:\n{e.stderr}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def create_account(user_name, password, full_name, description="None"):
        """Creates a new local user account."""
        print(f"Creating user: {user_name}")
        account_cmd = [
            "powershell", "-Command",
            f"New-LocalUser -Name '{user_name}' "
            f"-Password (ConvertTo-SecureString '{password}' -AsPlainText -Force) "
            f"-FullName '{full_name}' -Description '{description}'"
        ]
        WinMan.execute(account_cmd)

    @staticmethod
    def delete_user(user_name):
        """Deletes a local user account."""
        print(f"Deleting user: {user_name}")
        delete_cmd = ["net", "user", user_name, "/delete"]
        WinMan.execute(delete_cmd)

    @staticmethod
    def list_users():
        """Lists all local user accounts."""
        print("Listing local users...")
        list_cmd = ["net", "user"]
        WinMan.execute(list_cmd)

    @staticmethod
    def user_exists(user_name):
        """Checks if a local user exists."""
        print(f"Checking if user '{user_name}' exists...")
        get_users_cmd = ["net", "user"]
        output = WinMan.execute(get_users_cmd)
        if output and output.stdout:
            users = output.stdout.split()
            if user_name.lower() in [u.lower() for u in users]:
                print(f"User '{user_name}' exists.")
                return True
        print(f"User '{user_name}' not found.")
        return False

    @staticmethod
    def get_account_details(user_name):
        """Gets detailed information about a local user account."""
        print(f"Getting details for user: {user_name}")
        details_cmd = ["net", "user", user_name]
        WinMan.execute(details_cmd)

    @staticmethod
    def rename_user(old_name, new_name):
        """Renames a local user account."""
        print(f"Renaming user '{old_name}' to '{new_name}'")
        rename_cmd = [
            "powershell", "-Command",
            f"Rename-LocalUser -Name '{old_name}' -NewName '{new_name}'"
        ]
        WinMan.execute(rename_cmd)

    @staticmethod
    def change_password(user_name, new_password):
        """Changes the password for a local user."""
        print(f"Changing password for user: {user_name}")
        pass_cmd = [
            "powershell", "-Command",
            f"Set-LocalUser -Name '{user_name}' -Password "
            f"(ConvertTo-SecureString '{new_password}' -AsPlainText -Force)"
        ]
        WinMan.execute(pass_cmd)

    @staticmethod
    def user_groups(user_name):
        """Lists the groups a user is a member of."""
        print(f"Getting groups for user: {user_name}")
        groups_cmd = [
            "powershell", "-Command",
            f"(Get-LocalUser -Name '{user_name}').MemberOf"
        ]
        WinMan.execute(groups_cmd)

    @staticmethod
    def add_user_to_group(user_name, group_name):
        """Adds a user to a local group."""
        print(f"Adding user '{user_name}' to group '{group_name}'")
        add_cmd = [
            "powershell", "-Command",
            f"Add-LocalGroupMember -Group '{group_name}' -Member '{user_name}'"
        ]
        WinMan.execute(add_cmd)

    @staticmethod
    def remove_user_from_group(user_name, group_name):
        """Removes a user from a local group."""
        print(f"Removing user '{user_name}' from group '{group_name}'")
        remove_cmd = [
            "powershell", "-Command",
            f"Remove-LocalGroupMember -Group '{group_name}' -Member '{user_name}'"
        ]
        WinMan.execute(remove_cmd)

def show_help():
    """Displays the help message with available commands."""
    help_text = """
    Available commands:
    - makeuser [username] [password] [fullname] "[description]" : Create a new user.
    - delete_user [username] : Delete a user.
    - list_users : List all local users.
    - check_user [username] : Check if a user exists.
    - user_details [username] : Show detailed info of a user.
    - rename_user [oldname] [newname] : Rename a user account.
    - change_password [username] [newpassword] : Change a user's password.
    - user_groups [username] : List groups a user belongs to.
    - add_user_to_group [username] [groupname] : Add a user to a group.
    - remove_user_from_group [username] [groupname] : Remove a user from a group.
    - help : Show this help message.
    - exit, quit : Exit the program.

    Note: Arguments with spaces should be enclosed in double quotes.
    """
    print(help_text)

def main():
    """Main function to run the interactive command loop."""
    elevate_privileges()

    print("\nWelcome to WinManUtil - Windows User Management Utility")
    print("Type 'help' for a list of commands.")

    while True:
        try:
            cinput = input("> ").strip()
            if not cinput:
                continue
            if cinput.lower() in ["exit", "quit"]:
                break

            parts = shlex.split(cinput)
            command = parts[0].lower()
            args = parts[1:]

            def validate_args(expected_count):
                if len(args) != expected_count:
                    print(f"Error: Invalid number of arguments for '{command}'. Expected {expected_count}, got {len(args)}.")
                    return False
                return True

            if command == "makeuser":
                if len(args) < 3 or len(args) > 4:
                    print("Error: Usage: makeuser [username] [password] [fullname] \"[description]\"")
                    continue
                description = args[3] if len(args) == 4 else "None"
                WinMan.create_account(args[0], args[1], args[2], description)
            elif command == "delete_user":
                if validate_args(1):
                    WinMan.delete_user(args[0])
            elif command == "list_users":
                if validate_args(0):
                    WinMan.list_users()
            elif command == "check_user":
                if validate_args(1):
                    WinMan.user_exists(args[0])
            elif command == "user_details":
                if validate_args(1):
                    WinMan.get_account_details(args[0])
            elif command == "rename_user":
                if validate_args(2):
                    WinMan.rename_user(args[0], args[1])
            elif command == "change_password":
                if validate_args(2):
                    WinMan.change_password(args[0], args[1])
            elif command == "user_groups":
                if validate_args(1):
                    WinMan.user_groups(args[0])
            elif command == "add_user_to_group":
                if validate_args(2):
                    WinMan.add_user_to_group(args[0], args[1])
            elif command == "remove_user_from_group":
                if validate_args(2):
                    WinMan.remove_user_from_group(args[0], args[1])
            elif command == "help":
                show_help()
            else:
                print("Invalid command. Type 'help' for a list of commands.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")

if __name__ == "__main__":
    main()
