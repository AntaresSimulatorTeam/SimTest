import argparse
from pathlib import Path

import antares_test_utils as antares_utils
from run_command_building import *
import sys

parser = argparse.ArgumentParser()
parser.add_argument("batch_name", help="Directory containing studies",
                    type=str)

parser.add_argument("path_where_to_find_exe", help="Path to binary to exe",
                    type=str)

args = parser.parse_args()
batch_name = args.batch_name
batch_directory = Path(batch_name).resolve()

exe_path = find_binary(args.path_where_to_find_exe, batch_name)
print(f"Found executabled : {exe_path}")

study_path_collection = antares_utils.list_studies(batch_directory)

ret = []
for study_path in study_path_collection:
    print(study_path.name + '...', end='')

    antares_utils.remove_possibly_remaining_outputs(study_path)
    antares_utils.enable_study_output(study_path, True)

    command_to_run = make_command_to_run(exe_path, study_path)
    result = antares_utils.run_command(command_to_run)
    ret.append(result)
    print('OK' if result else 'KO')

    antares_utils.move_output_to_reference(study_path)

sys.exit(not all(ret))
