import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:

        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif os.path.isdir(target_dir):
            file_list = os.listdir(target_dir)
            final_string = ""
            for i in range(len(file_list)):
                file_path = os.path.normpath(os.path.join(target_dir, file_list[i]))
                final_string += f"- {file_list[i]}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
                if (i+1) < len(file_list):
                    final_string += "\n"
            return final_string
        else:
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
