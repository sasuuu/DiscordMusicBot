import json

def read_configuration(config_file_path):
    with open(config_file_path, "r") as f:
        return json.load(f)