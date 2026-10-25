import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        valid_target = os.path.commonpath([working_dir_abspath, file_abspath]) == working_dir_abspath



        if not valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(file_abspath):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
        with open(file_abspath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file. Additionally checks and creates directories to the file path if needed.",
        "parameters": {
            "type": "object",
            "file_path": "string",
            "content": "string",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "file_path": {
                    "type": "string",
                    "description": "File path to the file relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "Content string to be written into the designated file"
                },
            },
            "required":["file_path", "content"]
        },
    },
}
