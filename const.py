CHECK_USERNAME_PATTERN = r'^[a-zA-Z0-9]+$'

COMMAND_SERVE = "serve"
COMMAND_CREATE_USER = "createuser"
COMMAND_DELETE_USER = "deleteuser"
COMMAND_RESET_USER_TOKEN = "resetusertoken"

RESP_NOT_LOGIN = {"detail": "You do not have permission to perform this action."}
RESP_NOT_FOUND = {"detail": "Not found."}
