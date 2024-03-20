from pathlib import Path
import sys

def find_binary(path, batch_name):
    exe_identifier = "solver"
    if batch_name == "ts-generator":
        exe_identifier = batch_name

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
            # print(f"antares-{exe_identifier}{suffix}")
            # print("-")
            # print(path_item.name)
            # print("---")
            if path_item.is_file() and (f"antares-{exe_identifier}{suffix}" == path_item.name):
                results.append(path_item)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing {binary_name}")

def solver_config(study_name):
    if study_name == "valid-milp":
        return ("coin", True)
    else:
        return ("sirius", False)

def make_command_to_run(exe_path, study_path):

    if "ts-generator" in exe_path.name:
        cluster_to_gen_file = open(study_path / "clustersToGen.txt", 'r')
        cluster_to_gen = cluster_to_gen_file.readline().rstrip()  # remove new line char
        cluster_to_gen_file.close()
        command = [exe_path, cluster_to_gen, str(study_path)]
    else:
        # Do we need named MPS problems ?
        named_mps_problems = (study_path.parent.name == 'valid-named-mps')

        (opt_solver, use_ortools) = solver_config(study_path.parent.name)
        solver_path_full = str(Path(exe_path).resolve())

        command = [solver_path_full, "-i", str(study_path)]
        if use_ortools:
            command.append('--use-ortools')
            command.append('--ortools-solver=' + opt_solver)
        if named_mps_problems:
            command.append('--named-mps-problems')

    return command