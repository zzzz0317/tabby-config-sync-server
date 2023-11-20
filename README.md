# Tabby Config Sync Server

A tabby web service that only includes sync function

-----

## Run with waitress

```shell
$ waitress-serve --host 0.0.0.0 main:app
```

## Run with waitress and systemd

```ini
[Unit]
Description = Tabby Config Sync Server
After = network.target

[Service]
User = www-data
Group = www-data

WorkingDirectory = /var/www/tabby-config-sync-server
ExecStart = waitress-serve --host 0.0.0.0 --port 8001 main:app

Restart = on-failure
StartLimitInterval = 60s
StartLimitBurst = 5

[Install]
WantedBy = default.target
```

## Command line usage

```shell
$ python main.py -h
usage: main.py [-h] {serve,createuser,enableuser,deleteuser,resetusertoken} ...

Tabby Config Sync Server

positional arguments:
  {serve,createuser,enableuser,deleteuser,resetusertoken}
    serve               Start HTTP server
    createuser          Create user
    enableuser          Enable/Disable user
    deleteuser          Delete user
    resetusertoken      Reset user's config_sync_token

options:
  -h, --help            show this help message and exit
```

```shell
$ python main.py serve -h 
usage: main.py serve [-h] [--host HOST] [--port PORT] [--ssl] [--sslcrt SSLCRT] [--sslkey SSLKEY]

options:
  -h, --help       show this help message and exit
  --host HOST      HTTP listen host
  --port PORT      HTTP listen port
  --ssl            Use SSL
  --sslcrt SSLCRT  SSL certificate
  --sslkey SSLKEY  SSL key
```

```shell
$ python main.py serve -h 
usage: main.py serve [-h] [--host HOST] [--port PORT] [--ssl] [--sslcrt SSLCRT] [--sslkey SSLKEY]

options:
  -h, --help       show this help message and exit
  --host HOST      HTTP listen host
  --port PORT      HTTP listen port
  --ssl            Use SSL
  --sslcrt SSLCRT  SSL certificate
  --sslkey SSLKEY  SSL key
```

```shell
$ python main.py createuser -h 
usage: main.py createuser [-h] [--token TOKEN] username

positional arguments:
  username       User's name, unique

options:
  -h, --help     show this help message and exit
  --token TOKEN  config_sync_token, default is auto generate
```

```shell
$ python main.py enableuser -h 
usage: main.py enableuser [-h] [--disable] username

positional arguments:
  username    User's name

options:
  -h, --help  show this help message and exit
  --disable   Disable user
```

```shell
$ python main.py deleteuser -h 
usage: main.py deleteuser [-h] username

positional arguments:
  username    User's name

options:
  -h, --help  show this help message and exit
```

```shell
$ python main.py resetusertoken -h  
usage: main.py resetusertoken [-h] [--token TOKEN] username

positional arguments:
  username       User's name

options:
  -h, --help     show this help message and exit
  --token TOKEN  config_sync_token, default is auto generate
```