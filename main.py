import ctypes
import subprocess
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Script is not running with administrator privileges.")
    # Relaunch the script with admin rights
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    try:
        subprocess.run(['powershell', 'Start-Process', sys.executable, '-ArgumentList', params, '-Verb', 'runAs'], check=True)
    except subprocess.CalledProcessError:
        print("Failed to elevate privileges. Exiting.")
    sys.exit(0)

class WinUser:
    def __init__(self, user_name=None, password=None, full_name=None, description="None"):
        self.user_name = user_name
        self.password = password
        self.full_name = full_name
        self.description = description


    def create_account(self):
        account = [
            "powershell", "-Command",
            f"New-LocalUser -Name '{self.user_name}' "
            f"-Password (ConvertTo-SecureString '{self.password}' -AsPlainText -Force) "
            f"-FullName '{self.full_name}' -Description '{self.description}'"
        ]
        self.execute(account)

    def delete_user(self, user_name):
        delete = ["net", "user", f'{user_name}', "/delete"]
        self.execute(delete)

    def list_users(self):
        get_users = ["net", "user"]
        output = self.execute(get_users)
        return output.stdout if output else ""

    def user_exists(self, user_name=None, show_user_details=False):
        output = self.list_users().split()
        trimmed_result = [x.lower() for x in output if x.strip()]
        for result in trimmed_result:
            if user_name.lower() == result:
                if show_user_details:
                    return self.get_account_details(user_name).stdout
                return f"User {user_name} exists"
        return f"User {user_name} not found"

    def get_account_details(self, user_name):
        return self.execute(["net", "user", f'{user_name}'])

    def rename_user(self, old_name, new_name):
        rename_cmd = [
            "powershell", "-Command",
            f"Rename-LocalUser -Name '{old_name}' -NewName '{new_name}'"
        ]
        self.execute(rename_cmd)

    def change_password(self, user_name, new_password):
        pass_cmd = [
            "powershell", "-Command",
            f"Set-LocalUser -Name '{user_name}' -Password "
            f"(ConvertTo-SecureString '{new_password}' -AsPlainText -Force)"
        ]
        self.execute(pass_cmd)

    def user_groups(self, user_name):
        groups_cmd = [
            "powershell", "-Command",
            f"(Get-LocalUser -Name '{user_name}').MemberOf"
        ]
        output = self.execute(groups_cmd)
        if output:
            print(output.stdout)
        else:
            print("No groups found or user does not exist.")

    def add_user_to_group(self, user_name, group_name):
        add_cmd = [
            "powershell", "-Command",
            f"Add-LocalGroupMember -Group '{group_name}' -Member '{user_name}'"
        ]
        self.execute(add_cmd)

    def remove_user_from_group(self, user_name, group_name):
        remove_cmd = [
            "powershell", "-Command",
            f"Remove-LocalGroupMember -Group '{group_name}' -Member '{user_name}'"
        ]
        self.execute(remove_cmd)

    def execute(self, command):
        try:
            run = subprocess.run(command, check=True, capture_output=True, text=True)
            if run.returncode == 0:
                print(f"Successfully executed command {command}")
                return run
            else:
                print(run.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed. Command: {e.cmd} Return Code: {e.returncode}")
        except Exception as e:
            print(f"Error: {e}")

print("Welcome to WinMan\n")
print(
    "Enter Commands below, example: makeuser[username password fullname description]\n"
    "makeuser admin 123 Administrator An account with admin rights\n"
    "Commands should be separated by a space\n"
    "Additional commands: list_users, check_user [username], user_details [username], rename_user [oldname] [newname],\n"
    "change_password [username] [newpassword], user_groups [username], add_user_to_group [username] [groupname], remove_user_from_group [username] [groupname],\nhelp, exit, quit"
)

user = WinUser()

def show_help():
    help_text = """
Available commands:
- makeuser [username password fullname description] : Create a new user
- delete_user [username] : Delete a user
- list_users : List all local users
- check_user [username] : Check if a user exists
- user_details [username] : Show detailed info of a user
- rename_user [oldname] [newname] : Rename a user account
- change_password [username] [newpassword] : Change a user's password
- user_groups [username] : List groups a user belongs to
- add_user_to_group [username] [groupname] : Add a user to a group
- remove_user_from_group [username] [groupname] : Remove a user from a group
- help : Show this help message
- exit, quit : Exit the program
"""
    print(help_text)

while True:
    cinput = input("> ").strip()
    if cinput.lower() in ["exit", "quit"]:
        exit(0)
    user_input_split = cinput.split(" ")
    match user_input_split[0]:
        case "makeuser":
            trimmed_result = [x.strip() for x in user_input_split if x.strip()]
            if len(trimmed_result) < 5:
                print("Error: Invalid input format. Please provide all required fields.")
                continue
            final_trim = trimmed_result[:4] + [" ".join(trimmed_result[4:])]
            user.user_name = final_trim[1]
            user.password = final_trim[2]
            user.full_name = final_trim[3]
            user.description = final_trim[4]
            user.create_account()

        case "delete_user":
            if len(user_input_split) != 2:
                print(f"Error: Invalid input format. Expect 2 items got {len(user_input_split)}")
                continue
            user.delete_user(user_input_split[1])

        case "list_users":
            output = user.list_users()
            print(output)

        case "check_user":
            if len(user_input_split) != 2:
                print("Error: Username required")
                continue
            print(user.user_exists(user_input_split[1], show_user_details=False))

        case "user_details":
            if len(user_input_split) != 2:
                print("Error: Username required")
                continue
            details = user.get_account_details(user_input_split[1])
            if details:
                print(details.stdout)
            else:
                print("User details not found")

        case "rename_user":
            if len(user_input_split) != 3:
                print("Usage: rename_user [oldname] [newname]")
                continue
            user.rename_user(user_input_split[1], user_input_split[2])

        case "change_password":
            if len(user_input_split) != 3:
                print("Usage: change_password [username] [newpassword]")
                continue
            user.change_password(user_input_split[1], user_input_split[2])

        case "user_groups":
            if len(user_input_split) != 2:
                print("Usage: user_groups [username]")
                continue
            user.user_groups(user_input_split[1])

        case "add_user_to_group":
            if len(user_input_split) != 3:
                print("Usage: add_user_to_group [username] [groupname]")
                continue
            user.add_user_to_group(user_input_split[1], user_input_split[2])

        case "remove_user_from_group":
            if len(user_input_split) != 3:
                print("Usage: remove_user_from_group [username] [groupname]")
                continue
            user.remove_user_from_group(user_input_split[1], user_input_split[2])

        case "help":
            show_help()

        case _:
            print("Invalid command. Type 'help' for a list of commands.")
