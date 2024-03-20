import argparse
from pathlib import Path

import antares_test_utils as antares_utils
from run_comand_building import *
import sys

parser = argparse.ArgumentParser()
parser.add_argument("batch_directory", help="Directory containing studies",
                    type=str)

parser.add_argument("path_where_to_find_exe", help="Path to binary to exe",
                    type=str)

args = parser.parse_args()
batch_directory = Path(args.batch_directory).resolve()

solver_path = find_binary(args.path_where_to_find_exe, "solver")
print(f"Found exe to run {solver_path}")

ts_generator_path = find_binary(args.path_where_to_find_exe, "ts-generator")
print(f"Found ts-generator {ts_generator_path}")

study_path_collection = antares_utils.list_studies(batch_directory)

ret = []
for study_path in study_path_collection:
    print(study_path.name + '...', end='')

    antares_utils.remove_possibly_remaining_outputs(study_path)
    antares_utils.enable_study_output(study_path, True)

    command_to_run = make_command_to_run(solver_path, study_path, ts_generator_path)
    result = antares_utils.run_command(command_to_run)
    ret.append(result)
    print('OK' if result else 'KO')

    antares_utils.move_output_to_reference(study_path)

sys.exit(not all(ret))
