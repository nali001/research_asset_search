import shutil

def copy_files_from_list(file_list, source_dir, destination_dir):
    with open(file_list, 'r') as file:
        for line in file:
            filename = line.strip()
            source_file = source_dir + '/' + filename
            destination_file = destination_dir + '/' + filename
            shutil.copy2(source_file, destination_file)

# Example usage
file_list = './notebook_lists.txt'
source_dir = '../data/notebook/Kaggle/raw_notebooks'
destination_dir = './notebook/Kaggle/raw_notebooks'

copy_files_from_list(file_list, source_dir, destination_dir)
