from pathlib import Path
import os
import glob
import shutil
import subprocess

from study import Study

def list_directories(directory):
    dir_path = Path(directory)
    assert(dir_path.is_dir())
    dir_list = []
    for x in dir_path.iterdir():
        if x.is_dir():
            dir_list.append(x)
    return dir_list

def find_output_result_dir(output_dir):
    list_output_dir = list_directories(output_dir)
    assert len(list_output_dir) == 1

    list_dir = list_directories(list_output_dir[0])

    dir_list = []
    for x in list_dir:
        dir_path = Path(x)
        if dir_path.is_dir() and (dir_path.name == "adequacy" or dir_path.name == "economy" or dir_path.name == "adequacy-draft"):
            dir_list.append(x)
    assert len(dir_list) == 1
    return dir_list[0]

def get_headers(df) -> set :
    return set(df.columns)

def remove_outputs(study_path):
    output_path = study_path / 'output'
    files = glob.glob(str(output_path))
    for f in files:
        shutil.rmtree(f)

def launch_solver(solver_path, study_path, use_ortools = False, ortools_solver = "sirius"):
    # Clean study output
    remove_outputs(study_path)

    solver_path_full = str(Path(solver_path).resolve())

    command = [solver_path_full, "-i", str(study_path)]
    if use_ortools:
        command.append('--use-ortools')
        command.append('--ortools-solver='+ortools_solver)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
    output = process.communicate()

    return "Solver returned error" not in output[0].decode('iso-8859-1')

def generate_reference_values(solver_path, path, use_ortools, ortools_solver):

    enable_study_output(path,True)

    result = launch_solver(solver_path,path, use_ortools, ortools_solver)

    output_path = path / 'output'
    result_dir = find_output_result_dir(output_path)

    reference_path = path / 'output' / 'reference' / result_dir.name
    shutil.move(result_dir, reference_path)
    return result

def enable_study_output(study_path, enable):
    st = Study(str(study_path))
    st.check_files_existence()

    synthesis_value = "true" if enable else "false"
    st.set_variable(variable = "synthesis", value = synthesis_value, file_nick_name="general")

