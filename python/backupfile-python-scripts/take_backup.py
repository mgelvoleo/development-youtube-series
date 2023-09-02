import os
import time
import subprocess

con_exist = 0

def check_dir(os_dir):
    if not os.path.exists(os_dir):
        print(os_dir, "does not exist.")
        exit(1)

def ask_for_confirm():
    ans = input('Do you want to Continue? yes/no\n')
    global con_exist

    if ans == 'yes':
        con_exist = 0
    elif ans == 'no':
        con_exist = 1
    else:
        print('Answer with yes or no.')
        ask_for_confirm()

def create_remote_dir(remote_path):
    subprocess.run(['ssh', remote_path.split(':')[0], 'mkdir', '-p', remote_path.split(':')[1]])

def rsync_backup(source, destination):
    # Properly formatted rsync command
    subprocess.run(['rsync', '-av', '--delete', '--exclude=lost-found', '--exclude=/sys', '--exclude=/tmp',
                    '--exclude=/proc', '--exclude=/mnt', '--exclude=/dev', '--exclude=/backup',
                    source, destination])

backup_dir = input("Enter directory to backup\n")
check_dir(backup_dir)
print(backup_dir, "saved")
time.sleep(3)

backup_to_dir = input("Where to backup?\n")

check_dir(backup_to_dir)
print("Doing the backup now!")

ask_for_confirm()

if con_exist == 1:
    print("Abort the backup process!")
    exit(1)

# Creating the remote directory only if the user confirms
create_remote_dir(backup_to_dir)

rsync_backup(backup_dir, backup_to_dir)
