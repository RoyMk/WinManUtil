# WinManUtil

**WinManUtil** (Windows User Management Utility) is a robust Python-based command-line interface designed to streamline the management of local user accounts and groups on Windows. By leveraging PowerShell and native Windows commands, it provides IT administrators and power users with a centralized, interactive environment for automation and quick account operations.

---

## Features

- **User Account Management**:
  - Create new local users with full name and description.
  - Delete existing user accounts safely.
  - Rename user accounts seamlessly.
  - Update user passwords securely.
- **Information & Discovery**:
  - List all local user accounts.
  - Check for the existence of specific users.
  - Retrieve detailed account information (SID, password last set, etc.).
- **Group Management**:
  - View group memberships for any user.
  - Add users to local groups (e.g., Administrators, Users).
  - Remove users from local groups.
- **Seamless Elevation**: 
  - Automatically detects and requests Administrator privileges upon launch to ensure all operations succeed.

---

## Getting Started

### Prerequisites

- **Operating System**: Windows 10/11 or Windows Server.
- **Python**: 3.6+ (if running from source).
- **Permissions**: The utility requires Administrator privileges.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/WinManUtil.git
   cd WinManUtil
   ```

2. **Run from Source**:
   ```bash
   python main.py
   ```

3. **Build Executable (Optional)**:
   If you want a standalone `.exe`, use PyInstaller:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile main.py
   ```
   The executable will be generated in the `dist/` folder.

---

## Usage Guide

Once launched, WinManUtil provides an interactive prompt `>`.

### Common Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `makeuser` | Create a new user | `makeuser johndoe P@ssw0rd123 "John Doe" "Developer Account"` |
| `delete_user` | Delete a user | `delete_user johndoe` |
| `list_users` | List all local users | `list_users` |
| `check_user` | Check if user exists | `check_user johndoe` |
| `user_details` | Detailed info | `user_details johndoe` |
| `rename_user` | Rename account | `rename_user oldname newname` |
| `change_password` | Set new password | `change_password johndoe NewPass123` |
| `user_groups` | List user groups | `user_groups johndoe` |
| `add_user_to_group` | Add to group | `add_user_to_group johndoe Administrators` |
| `remove_user_from_group` | Remove from group | `remove_user_from_group johndoe Administrators` |
| `help` | Show help menu | `help` |
| `exit` / `quit` | Close utility | `exit` |

> **Note**: For `makeuser`, if the description contains spaces, ensure it is the last argument.

---

## Technical Details

- **Admin Elevation**: Uses `ctypes.windll.shell32.IsUserAnAdmin()` to check privileges and `ShellExecuteEx` (via PowerShell) to relaunch with the `runAs` verb if needed.
- **Backend**: Utilizes a mix of `net user` commands for speed and PowerShell cmdlets (`New-LocalUser`, `Set-LocalUser`, `Add-LocalGroupMember`) for modern features and robustness.

---

## Disclaimer

This tool performs system-level changes. Use it responsibly. Always verify user names and group names before executing deletion or modification commands.

---

## License

This project is open-source. Feel free to use and modify it as per your needs.
