import os

work_dir = os.getcwd()
num = 0
while os.path.exists(os.path.join(work_dir, chr(ord('A') + num))):
    question_path = os.path.join(work_dir, chr(ord('A') + num))
    test_num = 1
    folder_path_result = os.path.join(work_dir, 'result', chr(ord('A') + num))
    if not os.path.isdir(folder_path_result):
        os.mkdir(folder_path_result)
        os.mkdir(os.path.join(folder_path_result, 'in'))
        os.mkdir(os.path.join(folder_path_result, 'out'))
    while os.path.exists(os.path.join(question_path, f'{test_num}.in')) and os.path.exists(os.path.join(question_path, f'{test_num}.ans')):
        source_input_file = os.path.join(question_path, f'{test_num}.in')
        source_output_file = os.path.join(question_path, f'{test_num}.ans')
        dest_input_file = os.path.join(folder_path_result, 'in', f'input{test_num}.txt')
        dest_output_file = os.path.join(folder_path_result, 'out', f'output{test_num}.txt')
        os.system(f'cp {source_input_file} {dest_input_file}')
        os.system(f'cp {source_output_file} {dest_output_file}')
        test_num += 1
    if os.path.exists(os.path.join(folder_path_result, 'problem.zip')):
        os.remove(os.path.join(folder_path_result, 'problem.zip'))
    os.system(f"cd {folder_path_result};zip -r -q problem.zip in out")
    num += 1