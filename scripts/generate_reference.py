import argparse

import antares_test_utils as antares_utils
from run_command_building import *
import sys

# Parsing command line args
parser = argparse.ArgumentParser()
parser.add_argument("batch_name", help="Batch directory (containing studies)",
                    type=str)
parser.add_argument("path_where_to_find_exe", help="Path to executable",
                    type=str)
# Storing command line args
args = parser.parse_args()
batch_name = args.batch_name
path_where_to_find_exe = Path(args.path_where_to_find_exe)

# Find exe path
if not path_where_to_find_exe.is_dir() and not path_where_to_find_exe.is_file():
    raise RuntimeError("Path where to find an executable does not exist")
exe_identifier = exe_id_from_batch_name(batch_name)
exe_path = find_exe_path(path_where_to_find_exe, exe_identifier)
print(f"Found executabled : {exe_path}")

# Looking for studies in batch directory
study_path_collection = antares_utils.find_studies_in_batch_dir(batch_name)

ret = []
for study_path in study_path_collection:
    print("Study : %s ... " % study_path.name)

    antares_utils.remove_possibly_remaining_outputs(study_path)
    antares_utils.enable_study_output(study_path, True)

    command_to_run = make_command_to_run(exe_path, batch_name, study_path)
    result = run_command(command_to_run)
    ret.append(result)
    print('OK' if result else 'KO')

    antares_utils.move_output_to_reference(study_path)

sys.exit(not all(ret))
