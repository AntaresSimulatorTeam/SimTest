import argparse
from pathlib import Path

import antares_test_utils as antares_utils
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
        for x in binary_path.iterdir():
            if x.is_file() and (f"antares-{binary_name}{suffix}" == x.name):
                results.append(x)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing {binary_name}")

def solver_config(study_name):
    if study_name == "valid-milp":
        return ("coin", True)
    else:
        return ("sirius", False)

def make_command(solver_path, study_path, ts_generator_path):
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

parser = argparse.ArgumentParser()
parser.add_argument("batch_directory", help="Directory containing studies",
                    type=str)

parser.add_argument("solver", help="Path to antares-solver",
                    type=str)

args = parser.parse_args()
batch_directory = Path(args.batch_directory).resolve()

solver_path = Path(args.solver).resolve()

solver_path = find_binary(args.solver, "solver")
print(f"Found solver {solver_path}")

ts_generator_path = find_binary(args.solver, "ts-generator")
print(f"Found ts-generator {ts_generator_path}")

study_patyh_collection = antares_utils.list_studies(batch_directory)

ret = []
for study_path in study_patyh_collection:
    print(study_path.name + '...', end='')

    antares_utils.remove_possibly_remaining_outputs(study_path)
    antares_utils.enable_study_output(study_path, True)

    command = make_command(solver_path, study_path, ts_generator_path)
    result = antares_utils.run_command(command)
    ret.append(result)
    print('OK' if result else 'KO')

    antares_utils.move_output_to_reference(study_path)

sys.exit(not all(ret))
