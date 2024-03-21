from pathlib import Path
import subprocess
import sys

def find_binary(path, exe_identifier):
    if sys.platform.startswith("win"):
        suffix=".exe"
    else:
        suffix=""

    binary_path = Path(path)
    if binary_path.is_file():
        return path.resolve()
    if binary_path.is_dir():
        results = []
        for path_item in binary_path.iterdir():
            if path_item.is_file() and (f"antares-{exe_identifier}{suffix}" == path_item.name):
                results.append(path_item)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing {binary_name}")

def make_command_to_run(path_where_to_find_exe, batch_name, study_path):
    command_to_run = []
    exe_path = Path()
    exe_identifier = "solver" # Default value

    if batch_name == "ts-generator":
        exe_identifier = "ts-generator"
        exe_path = find_binary(path_where_to_find_exe, exe_identifier)
        print(f"Found executabled : {exe_path}")

        cluster_to_gen_file = open(study_path / "clustersToGen.txt", 'r')
        cluster_to_gen = cluster_to_gen_file.readline().rstrip()
        cluster_to_gen_file.close()
        command_to_run = [exe_path, cluster_to_gen, str(study_path)]

    else:
        exe_path = find_binary(path_where_to_find_exe, exe_identifier)
        print(f"Found executabled : {exe_path}")

        command_to_run = [exe_path, "-i", str(study_path)]
        if batch_name == "valid-milp":
            command_to_run.append('--use-ortools')
            command_to_run.append('--ortools-solver=coin')

        if batch_name == "valid-named-mps":
            command_to_run.append('--named-mps-problems')

    return command_to_run

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
    process.communicate()
    exit_code = process.wait()
    return (exit_code == 0)