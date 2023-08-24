import os
import shutil
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
        return con_exist
    elif ans == 'no':
        con_exist = 1
        return con_exist
    else:
        print('Answer with yes or no.')
        ask_for_confirm()

def del_files(ending):
    for r, d, f in os.walk(backup_dir):
        for files in f:
            if files.endswith("." + ending):
                os.remove(os.path.join(r,files))


def rsync_backup(source, destination):
    # Properly formatted rsync command
    subprocess.run(['rsync', '-av', '--delete', '--exclude=lost-found', '--exclude=/sys', '--exclude=/tmp',
                    '--exclude=/proc', '--exclude=/mnt', '--exclude=/dev', '--exclude=/backup',
                    source, destination])

   

backup_dir = input("Enter directory to backup\n")
check_dir(backup_dir)
print(backup_dir,"saved")
time.sleep(3)

backup_to_dir= input("Where to backup?\n")

check_dir(backup_to_dir)
print ("Doing the backup now!")

ask_for_confirm()

if con_exist == 1:
    print("Abourtnig the backup process!")
    exit(1)

rsync_backup(backup_dir,backup_to_dir)
