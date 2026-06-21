import pathlib
import glob
import difflib

def read_file(path:str):
    """Read and return the contents of a file at the given path. Use absolute paths."""
    try:
        file_contents = pathlib.Path(path).read_text()
        return file_contents
    except Exception as e:
        return f"Error reading file: {e}"

def glob_files(pattern:str, recursive=True, include_hidden=True):
    """Find files matching a glob pattern. Use ** for recursive search. Use absolute paths in patterns when searching outside the current directory. Hidden files and directories are included by default. Returns a list of matching file paths."""
    try:
        files = glob.glob(pattern, recursive=recursive, include_hidden=include_hidden)
        return files
    except Exception as e:
        return f"Glob error: {e}"

def create_file(path:str, content:str):
    """Create a file at the given path with the provided content. Use absolute paths. Overwrites if the file already exists."""
    try:
        file = pathlib.Path(path).write_text(content)
        return f"File created: {path}"
    except Exception as e:
        return f"Error creating file: {e}"

def edit_file(path:str, edits:list[dict]):
    """Edit a file by replacing strings. Each edit is a dict with 'old' and 'new' keys. old must exactly match existing text in the file, including whitespace. Use absolute paths. Always read the file before calling this. Returns a unified diff of all changes."""
    try:
        content = pathlib.Path(path).read_text()
        new_content = content
        for edit in edits:
            new_content = new_content.replace(edit["old"], edit["new"])
        diff = list(difflib.unified_diff(
            content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=path,
            tofile=path,
        ))
        pathlib.Path(path).write_text(new_content)
        return {"path": path, "diff": "".join(diff)}
    except Exception as e:
        return f"Error editing file: {e}"

def rename_file(current_path:str, new_filename:str):
    """Rename a file. current_path is the absolute path to the existing file, new_filename is just the new name (not a full path). Returns a confirmation string."""
    try:
        file_path = pathlib.Path(current_path)
        file_path.rename(file_path.parent / new_filename)
        return f"Succesfully renamed {current_path} to {new_filename}"
    except Exception as e:
        return f"Error renaming file: {e}"
