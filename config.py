import json

with open("config.json", "r", encoding="utf-8") as f_config_json:
    config_data = json.load(f_config_json)

http_config_data = config_data.get("http", {})
http_listen_host = config_data.get("listen_host", "127.0.0.1")
http_listen_port = int(config_data.get("listen_port", 8001))
http_ssl = config_data.get("ssl", False)
http_ssl_crt = config_data.get("ssl_crt", None)
http_ssl_key = config_data.get("ssl_key", None)

sync_config_data = config_data.get("sync", {})
sync_save_old = sync_config_data.get("save_old", False)
