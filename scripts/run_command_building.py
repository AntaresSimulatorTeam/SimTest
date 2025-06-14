from pathlib import Path
import subprocess
import sys

def find_exe_path(path_to_search_exe_in, exe_identifier):
    searched_exe = f"antares-{exe_identifier}"
    if sys.platform.startswith("win"):
        searched_exe += ".exe"

    if path_to_search_exe_in.is_file() and path_to_search_exe_in.name == searched_exe:
        return path_to_search_exe_in.resolve()
    for path_item in path_to_search_exe_in.iterdir():
        if path_item.is_file() and (path_item.name == searched_exe):
            return path_item.resolve()
    raise RuntimeError("Missing {searched_exe}")

def make_command_to_run(path_where_to_find_exe, batch_name, study_path):
    command_to_run = []
    exe_path = Path()
    exe_identifier = "solver" # Default value

    exe_path = find_exe_path(path_where_to_find_exe, exe_identifier)
    print(f"Found executabled : {exe_path}")

    command_to_run = [exe_path, "-i", str(study_path)]
    if batch_name == "valid-milp":
        command_to_run.append('--solver=coin')

    if batch_name == "valid-named-mps":
        command_to_run.append('--named-mps-problems')

    return command_to_run

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
    process.communicate()
    exit_code = process.wait()
    return (exit_code == 0)
