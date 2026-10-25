import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        valid_target = os.path.commonpath([working_dir_abspath, file_abspath]) == working_dir_abspath



        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(file_abspath):
            with open(file_abspath, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string

        else:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns content of a file as a string with a maximum character limit, providing additional message if the content has been truncated",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path":{
                    "type": "string",
                    "description": "String containing the file path to read, relative to the working directory"
                },
            },
            "required":["file_path"]
        },
    },
}
