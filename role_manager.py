# role_manager.py

import os

class RoleManager:
    def __init__(self, file_name='admin_roles.txt'):
        """Initialize the role manager with a file name."""
        self.file_name = file_name
        self.load_roles()

    def load_roles(self):
        """Load roles from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.roles = [int(line.strip()) for line in file]
        else:
            self.roles = []

    def save_roles(self):
        """Save roles to the file."""
        with open(self.file_name, 'w') as file:
            for role in self.roles:
                file.write(f"{role}\n")

    def add_role(self, role_id):
        """Add a new role and save to file."""
        if role_id not in self.roles:
            self.roles.append(role_id)
            self.save_roles()
            return True
        return False

    def remove_role(self, role_id):
        """Remove a role and save to file."""
        if role_id in self.roles:
            self.roles.remove(role_id)
            self.save_roles()
            return True
        return False

    def is_admin(self, user_roles):
        """Check if any of the user's roles are in the admin roles list."""
        return any(role.id in self.roles for role in user_roles)
    


class SubmissionRoleManager:
    def __init__(self, file_name='submission_roles.txt'):
        """Initialize the submission role manager with a file name."""
        self.file_name = file_name
        self.load_roles()

    def load_roles(self):
        """Load roles from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.roles = [int(line.strip()) for line in file]
        else:
            self.roles = []

    def save_roles(self):
        """Save roles to the file."""
        with open(self.file_name, 'w') as file:
            for role in self.roles:
                file.write(f"{role}\n")

    def add_role(self, role_id):
        """Add a new role and save to file."""
        if role_id not in self.roles:
            self.roles.append(role_id)
            self.save_roles()
            return True
        return False

    def remove_role(self, role_id):
        """Remove a role and save to file."""
        if role_id in self.roles:
            self.roles.remove(role_id)
            self.save_roles()
            return True
        return False

    def can_submit(self, user_roles):
        """Check if any of the user's roles are in the submission roles list."""
        return any(role.id in self.roles for role in user_roles)