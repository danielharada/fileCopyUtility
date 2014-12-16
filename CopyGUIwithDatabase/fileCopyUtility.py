import os
import time
import shutil
import glob


def reviewAndCopy(copy_from_directory, copy_to_directory, review_window_in_sec):
    os.chdir(copy_from_directory)
    text_files = getAllTxtFilesFromCurrentDirectory()
    files_with_age = createFileAgeDict(text_files)
    trimToOnlyModifiedInWindow(files_with_age, review_window_in_sec)
    files_to_copy = filesDictToFileList(files_with_age)

    deleteAllFilesInDirectory(copy_to_directory)
    copyFilesToTargetDirectory(files_to_copy, copy_to_directory)

def getAllTxtFilesFromCurrentDirectory():
    return glob.glob('*.txt')

def createFileAgeDict(file_list):
    files_with_age = {}
    now = time.time()
    for each_file in file_list:
        files_with_age[each_file] = findAgeSinceChange(each_file, now)

    return files_with_age

def findAgeSinceChange(single_file, time_to_check_age_against):
    try:
        modify_time = os.path.getmtime(single_file)
        create_time = os.path.getctime(single_file)
        change_time = max(modify_time, create_time)
        age_since_change = time_to_check_age_against - change_time

        return age_since_change
    except WindowsError:
        print('There was an error reading create/modify time from file ', single_file)

def trimToOnlyModifiedInWindow(files_with_age, time_window):
    for each_file in list(files_with_age.keys()):
        if files_with_age[each_file] > time_window:
            del files_with_age[each_file]

def filesDictToFileList(file_dict):
    return list(file_dict.keys())
    
def deleteAllFilesInDirectory(target_directory):
    current_directory = os.getcwd()
    os.chdir(target_directory)
    deleteAllFilesInCurrentDirectory()
    os.chdir(current_directory)

def deleteAllFilesInCurrentDirectory():
    current_directory = os.getcwd()
    for each_file in os.listdir(current_directory):
        try:
            os.remove(each_file)
        except WindowsError:
            print('There was an error deleting file ', each_file)
			
def copyFilesToTargetDirectory(files_to_copy, target_directory):
    for each_file in files_to_copy:
        try:
            shutil.copy2(each_file, target_directory)
        except WindowsError:
            print('There was an error copying file ', each_file)
            

if __name__ == '__main__':

    copy_from_directory = 'C:\\Users\\student\\Documents\\Python\\Drills\\FileCopyUtility\\Copy From'
    copy_to_directory = 'C:\\Users\\student\\Documents\\Python\\Drills\\FileCopyUtility\\Copy To'

    review_window = 24*3600

    reviewAndCopy(copy_from_directory, copy_to_directory, review_window)
    

    


    
