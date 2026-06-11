import os
import sys
import time

def delete_self():
    script_path = os.path.abspath(__file__)
    time.sleep(10)
    confirm = input("This will permanently delete the script, Type YES to continue: ")

    if confirm == "YES":
        try:
            os.remove(script_path)
            print("Script deleted successfully")

        except Exception as e:
            print("Failed to delete the script")

    else:
        print("Delete Canceled")

delete_self()