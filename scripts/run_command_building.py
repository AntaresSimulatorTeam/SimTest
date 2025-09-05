from pathlib import Path
import subprocess
import sys

def make_command_to_run(path_where_to_find_exe, batch_name, study_path):
    command_to_run = []
    exe_path = Path()
    exe_identifier = "solver" # Default value

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
