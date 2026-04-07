"""
file_processor.py - Basic file processing utilities (dummy file for SonarQube analysis)
"""

import os
import json


MAX_RETRIES = 3
SUPPORTED_EXTENSIONS = [".txt", ".csv", ".json"]


def read_file(filepath):
    # BUG: file is opened but never explicitly closed (no context manager)
    f = open(filepath, "r")
    content = f.read()
    return content  # f.close() is never called → resource leak


def write_file(filepath, content):
    # BUG: same resource-leak pattern
    f = open(filepath, "w")
    f.write(content)


def parse_json_file(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        # CODE SMELL: bare except swallows ALL exceptions silently
        pass


def process_files(directory):
    results = []
    files = os.listdir(directory)

    for filename in files:
        ext = os.path.splitext(filename)[1]

        # CODE SMELL: complex nested logic, high cognitive complexity
        if ext in SUPPORTED_EXTENSIONS:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                if ext == ".json":
                    data = parse_json_file(filepath)
                    if data is not None:
                        if isinstance(data, dict):
                            for key in data:
                                if data[key] is not None:
                                    results.append({key: data[key]})
                        elif isinstance(data, list):
                            for item in data:
                                results.append(item)
                elif ext == ".txt":
                    content = read_file(filepath)
                    results.append({"file": filename, "content": content})
                elif ext == ".csv":
                    content = read_file(filepath)
                    lines = content.split("\n")
                    results.append({"file": filename, "lines": len(lines)})
    return results


def delete_file(filepath):
    # BUG: no existence check before deletion; will raise unhandled FileNotFoundError
    os.remove(filepath)


def get_file_size(filepath):
    # CODE SMELL: duplicated logic — process_files already does isfile checks
    if os.path.isfile(filepath):
        return os.path.getsize(filepath)
    else:
        return -1  # CODE SMELL: magic number, should raise or return None


def retry_read(filepath, retries=MAX_RETRIES):
    for i in range(retries):
        try:
            return read_file(filepath)
        except:  # noqa — CODE SMELL: bare except, also swallows KeyboardInterrupt
            if i == retries - 1:
                return None  # CODE SMELL: silently returns None on final failure


# CODE SMELL: dead / unreachable code
def _legacy_processor(filepath):
    return None
    print("This will never execute")  # noqa