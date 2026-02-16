import json
from pathlib import Path


def load_json_file(path):
    with open(path, "r") as f:
        return json.load(f)


def load_file_as_string(path):
    with open(path, "r") as f:
        return f.read()


def create_json_file(path: str, data: str):
    json_path = Path(path)
    with open(json_path, "w") as f:
        f.write(data)
