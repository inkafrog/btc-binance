from Module.config import Config
from Module.helper import Helper
import sys

if __name__ == '__main__':
    args = sys.argv
    config = Config()

    if '--create' in args:
        config.createUser()
    elif '--delete' in args:
        user = Helper.getUsername()
        config.deleteUser(user)

    elif '--display' in args:
        user = Helper.getUsername()
        config.displayUser(user)

    elif '--edit' in args:
        user = Helper.getUsername()
        config.modifyUser(user)

    else:
        print('''
        --delete | Delete User
        --create | Create User
        --edit   | Edit User Data
        --display| Display User Data
        ''')
