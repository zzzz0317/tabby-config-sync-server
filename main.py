import argparse
import re

from flask import Flask, request, jsonify
from playhouse.shortcuts import model_to_dict

from const import *
from config import *
from models import User, Config, ConfigHistory
from util import *

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def get_config_by_user_and_config_id(user, config_id):
    try:
        return Config.get((Config.user == user) & (Config.id == config_id))
    except:
        return None


def get_user_by_config_sync_token(config_sync_token):
    try:
        return User.get((User.config_sync_token == config_sync_token) & User.enable)
    except:
        return None


def get_user_by_request(request):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        auth_type, token = authorization_header.split(' ')
        if auth_type == 'Bearer':
            return get_user_by_config_sync_token(token)
    return None


@app.route('/api/1/user', methods=['GET'])
def handle_get_user():
    user = get_user_by_request(request)
    if user is None:
        return jsonify(RESP_NOT_LOGIN)
    data = {
        "id": user.id,
        "username": user.username,
        "active_config": user.active_config,
        "custom_connection_gateway": None,
        "custom_connection_gateway_token": None,
        "config_sync_token": user.config_sync_token,
        "is_pro": True,
        "is_sponsor": False,
        "github_username": None
    }
    return jsonify(data)


@app.route('/api/1/configs', methods=['GET', 'POST'])
def handle_configs():
    user = get_user_by_request(request)
    if user is None:
        return jsonify(RESP_NOT_LOGIN)
    if request.method == 'GET':
        data_list = []
        data_query = Config.select().where((Config.user == user))
        for d in data_query:
            dd = model_to_dict(d)
            format_config_dict(dd)
            data_list.append(dd)
        return jsonify(data_list)
    elif request.method == 'POST':
        data = request.json
        name = data.get('name', None)
        content = data.get('content', "{}")
        last_used_with_version = data.get('last_used_with_version', None)
        obj = Config.create(user=user, name=name, content=content, last_used_with_version=last_used_with_version)
        dd = model_to_dict(obj)
        format_config_dict(dd)
        return jsonify(dd), 201


@app.route('/api/1/configs/<int:config_id>', methods=['GET', 'PATCH'])
def handle_single_config(config_id):
    user = get_user_by_request(request)
    if user is None:
        return jsonify(RESP_NOT_LOGIN)
    config = get_config_by_user_and_config_id(user, config_id)
    if not config:
        return jsonify(RESP_NOT_FOUND)
    if request.method == 'PATCH':
        data = request.json
        flag_is_changed = False
        old_config = model_to_dict(config)
        for k in ['name', 'content', 'last_used_with_version']:
            if k in data.keys():
                if getattr(config, k) != data[k]:
                    setattr(config, k, data[k])
                    flag_is_changed = True
        if flag_is_changed:
            if sync_save_old:
                ConfigHistory.create(
                    config=config,
                    name=old_config.get('name', ''),
                    content=old_config.get('name', '{}'),
                    last_used_with_version=old_config.get('last_used_with_version', None),
                    created_at=old_config['created_at']
                )
            config.save()
    return jsonify(format_config_dict(model_to_dict(config)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tabby Config Sync Server")
    subparsers = parser.add_subparsers(dest="command")

    parser_serve = subparsers.add_parser(COMMAND_SERVE, help="Start HTTP server")
    parser_serve.add_argument("--host", type=str, default=http_listen_host, help="HTTP listen host")
    parser_serve.add_argument("--port", type=int, default=http_listen_port, help="HTTP listen port")
    parser_serve.add_argument('--ssl', action="store_true", help='Use SSL')
    parser_serve.add_argument('--sslcrt', type=str, default=None, help="SSL certificate")
    parser_serve.add_argument('--sslkey', type=str, default=None, help="SSL key")

    parser_create_user = subparsers.add_parser(COMMAND_CREATE_USER, help="Create user")
    parser_create_user.add_argument("username", type=str, help="User\'s name, unique")
    parser_create_user.add_argument("--token", type=str, default="",
                                    help="config_sync_token, default is auto generate")

    parser_delete_user = subparsers.add_parser(COMMAND_DELETE_USER, help="Delete user")
    parser_delete_user.add_argument("username", type=str, help="User\'s name")

    parser_reset_user = subparsers.add_parser(COMMAND_RESET_USER_TOKEN, help="Reset user\'s config_sync_token")
    parser_reset_user.add_argument("username", type=str, help="User\'s name")
    parser_reset_user.add_argument("--token", type=str, default="",
                                   help="config_sync_token, default is auto generate")

    args = parser.parse_args()
    args_command = args.command

    if args_command == COMMAND_SERVE:
        if args.ssl:
            if args.sslcrt is None or args.sslkey is None:
                parser_serve.print_help()
                print("\nThe ssl certificate and private key were not specified!")
                exit(1)
            elif not os.path.exists(args.sslcrt):
                print("SSL certificate file", args.sslcrt, "not found")
                exit(1)
            elif not os.path.exists(args.sslkey):
                print("SSL private key file", args.sslkey, "not found")
                exit(1)
            else:
                app.run(host=args.host, port=args.port, ssl_context=(args.sslcrt, args.sslkey))
        else:
            app.run(host=args.host, port=args.port)
    elif args_command == COMMAND_CREATE_USER:
        username = args.username
        token = args.token
        if token == "":
            token = generate_token()
            print("Generated token is:")
            print(token)
        if not re.match(CHECK_USERNAME_PATTERN, username):
            raise Exception("Username has unexpected character")
        User.create(username=username, config_sync_token=token)
        print(f"Create user {username} success")
    elif args_command == COMMAND_DELETE_USER:
        username = args.username
        User.get(username=username).delete_instance()
        print(f"Delete user {username} success")
    elif args_command == COMMAND_RESET_USER_TOKEN:
        username = args.username
        token = args.token
        if token == "":
            token = generate_token()
            print("Generated token is:")
            print(token)
        user = User.get(username=username)
        user.config_sync_token = token
        user.save()
        print(f"Reset user {username}'s token success")
    else:
        parser.print_usage()
