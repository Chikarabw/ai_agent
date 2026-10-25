import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        valid_target = os.path.commonpath([working_dir_abspath, file_abspath]) == working_dir_abspath



        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(file_abspath):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_abspath]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, cwd=working_dir_abspath, text=True, timeout=30)

        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced\n"
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}\n"

        return output


    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file and executes code that returns applicable return codes, stdout, and stderr data as string output",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Additional command-line arguments only. Do not include the script path; it is already supplied in file_path. Omit args when the user requests no additional arguments."
                },
                "file_path":{
                    "type": "string",
                    "description": "String containing the file path to the python file to run"
                }
            },
            "required":["file_path"]
        },
    },
}
