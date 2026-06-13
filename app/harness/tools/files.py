import pathlib
import glob
import difflib

def read_file(path:str):
    """Read and return the contents of a file at the given 
    path."""
    try:
        file_contents = pathlib.Path(path).read_text()
        return file_contents
    except Exception as e:
        return f"Error reading file: {e}"

def glob_files(pattern:str, recursive=True, include_hidden=True):
    """Find files matching a glob pattern. Use ** for recursive
  search. Returns a list of matching file paths."""
    try:
        files = glob.glob(pattern, recursive=recursive, include_hidden=include_hidden)
        return files
    except Exception as e:
        return f"Glob error: {e}"

def create_file(path:str, content:str):
    """Create a file at the given path with the provided content.
  Overwrites if the file already exists."""
    try:
        file = pathlib.Path(path).write_text(content)
        return f"File created: {path}"
    except Exception as e:
        return f"Error creating file: {e}"

def edit_file(path:str, edits:list[dict]):
    """Edit a file by replacing strings. Each edit is a dict with 'old' and 'new' keys. Always read the file before calling this. Returns a unified diff of all changes."""
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
