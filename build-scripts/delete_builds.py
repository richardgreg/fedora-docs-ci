# importing the required modules
import os
import shutil
import time

# main function
def main():

	# specify the path
	path = "/var/www/html"

	# specify the days
	days = 15

	# convert the current day to seconds
	# time.time() returns current time since epoch (1970) in seconds
	days_in_seconds = days * 24 * 60 * 60

	# check whether the file is present in path or not
	if os.path.exists(path):
		# iterate over each list of folders in the path
		for root_folder, folders, _ in os.walk(path):
			for folder in folders:
				# folder path
				folder_path = os.path.join(root_folder, folder)
                # comparing with the days
				if time.time() - get_folder_age(folder_path) >= days_in_seconds:
                    # invoking the remove_folder function
					remove_folder(folder_path)
	else:
		# file/folder is not found
		print(f'"{path}" is not found')


def remove_folder(path):
	# removing the folder
	if not shutil.rmtree(path):
		# success message
		print(f"{path} is removed successfully")
	else:
		# failure message
		print(f"Unable to delete the {path}")


def get_folder_age(path):
	# getting ctime of the folder
	# time will be in seconds
	ctime = os.stat(path).st_ctime

	# returning the time
	return ctime


if __name__ == '__main__':
	main()