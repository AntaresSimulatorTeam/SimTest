from pathlib import Path
import glob
import shutil

from study import Study

def list_directories(directory):
    dir_path = Path(directory)
    assert(dir_path.is_dir())
    dir_list = []
    for x in dir_path.iterdir():
        if x.is_dir():
            dir_list.append(x)
    return dir_list

def find_studies_in_batch_dir(batch_name):
    batch_directory = Path(batch_name).resolve()
    studies = []
    if (batch_directory.is_dir()):
        study = Study(batch_directory)
        if study.check_files_existence():
            studies.append(batch_directory)
        else:
            for x in batch_directory.iterdir():
                studies.extend(find_studies_in_batch_dir(x))

    return studies

def get_headers(df) -> set :
    return set(df.columns)

def remove_possibly_remaining_outputs(study_path):
    output_path = study_path / 'output'
    files = glob.glob(str(output_path))
    for f in files:
        shutil.rmtree(f)

def move_output_to_reference(study_path):
    output_path = study_path / 'output'
    list_dir = list_directories(output_path) # list of 'output' sub-directories
    if len(list_dir) != 1 : # We should have only 1 results directory
        raise AssertionError("Too many results directories in output")
    result_dir = list_dir[0]
    reference_path = study_path / 'output' / 'reference'
    shutil.move(result_dir, reference_path)


def enable_study_output(study_path, enable):
    st = Study(study_path)
    if not st.check_files_existence():
        raise RuntimeError("Missing file")

    synthesis_value = "true" if enable else "false"
    st.set_variable(variable = "synthesis", value = synthesis_value, file_nick_name="general")

