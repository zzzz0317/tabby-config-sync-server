import os
import sys

DIR_SCRIPT = os.path.dirname(os.path.realpath(sys.argv[0]))
DIR_RUNNING = os.getcwd()

CHECK_USERNAME_PATTERN = r'^[a-zA-Z0-9]+$'

COMMAND_SERVE = "serve"
COMMAND_CREATE_USER = "createuser"
COMMAND_DELETE_USER = "deleteuser"
COMMAND_RESET_USER_TOKEN = "resetusertoken"

RESP_NOT_LOGIN = {"detail": "You do not have permission to perform this action."}
RESP_NOT_FOUND = {"detail": "Not found."}
