import argparse

import antares_test_utils as antares_utils
from run_command_building import *
import sys

# Parsing args
parser = argparse.ArgumentParser()
parser.add_argument("batch_name", help="Batch directory (containing studies)",
                    type=str)
parser.add_argument("path_where_to_find_exe", help="Path to executable",
                    type=str)
#  Storing args
args = parser.parse_args()
batch_name = args.batch_name
path_where_to_find_exe = Path(args.path_where_to_find_exe)

# Looking for studies in batch directory
study_path_collection = antares_utils.find_studies_in_batch_dir(batch_name)

ret = []
for study_path in study_path_collection:
    print("Study : %s ... " % study_path.name)

    antares_utils.remove_possibly_remaining_outputs(study_path)
    antares_utils.enable_study_output(study_path, True)

    command_to_run = make_command_to_run(path_where_to_find_exe, batch_name, study_path)
    result = run_command(command_to_run)
    ret.append(result)
    print('OK' if result else 'KO')

    antares_utils.move_output_to_reference(study_path)

sys.exit(not all(ret))
