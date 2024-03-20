from pathlib import Path
import sys

def find_binary(path, binary_name):
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
            if path_item.is_file() and (f"antares-{binary_name}{suffix}" == path_item.name):
                results.append(path_item)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing {binary_name}")

def solver_config(study_name):
    if study_name == "valid-milp":
        return ("coin", True)
    else:
        return ("sirius", False)

def make_command_to_run(solver_path, study_path, ts_generator_path):
    # Do we need named MPS problems ?
    named_mps_problems = (study_path.parent.name == 'valid-named-mps')

    # Are we testing the time series generator ?
    if study_path.parent.name != 'ts-generator':
        ts_generator_path = ""

    (opt_solver, use_ortools) = solver_config(study_path.parent.name)
    solver_path_full = str(Path(solver_path).resolve())

    command = [solver_path_full, "-i", str(study_path)]
    if use_ortools:
        command.append('--use-ortools')
        command.append('--ortools-solver=' + opt_solver)
    if named_mps_problems:
        command.append('--named-mps-problems')
    if ts_generator_path != "":
        cluster_to_gen_file = open(study_path / "clustersToGen.txt", 'r')
        cluster_to_gen = cluster_to_gen_file.readline().rstrip()  # remove new line char
        cluster_to_gen_file.close()
        command = [ts_generator_path, cluster_to_gen, str(study_path)]
    return command