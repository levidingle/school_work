import cv2
import pyautogui
import scipy
import sounddevice as sd
import os


RESET = "\033[0m"
BOLD = "\033[1m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright versions
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

def banner1():
    print(BRIGHT_MAGENTA + BOLD + r""" __     __     __     __         _____        __   __     ______     ______      __     __     ______     __     ______     _____        ______   ______     ______     __         ______    
/\ \  _ \ \   /\ \   /\ \       /\  __-.     /\ "-.\ \   /\  __ \   /\__  _\    /\ \  _ \ \   /\  ___\   /\ \   /\  == \   /\  __-.     /\__  _\ /\  __ \   /\  __ \   /\ \       /\  ___\   
\ \ \/ ".\ \  \ \ \  \ \ \____  \ \ \/\ \    \ \ \-.  \  \ \ \/\ \  \/_/\ \/    \ \ \/ ".\ \  \ \  __\   \ \ \  \ \  __<   \ \ \/\ \    \/_/\ \/ \ \ \/\ \  \ \ \/\ \  \ \ \____  \ \___  \  
 \ \__/".~\_\  \ \_\  \ \_____\  \ \____-     \ \_\\"\_\  \ \_____\    \ \_\     \ \__/".~\_\  \ \_____\  \ \_\  \ \_\ \_\  \ \____-       \ \_\  \ \_____\  \ \_____\  \ \_____\  \/\_____\ 
  \/_/   \/_/   \/_/   \/_____/   \/____/      \/_/ \/_/   \/_____/     \/_/      \/_/   \/_/   \/_____/   \/_/   \/_/ /_/   \/____/        \/_/   \/_____/   \/_____/   \/_____/   \/_____/ 
                                                                                                                                                                                             """ + RESET)


def screenshotcapture():
    image = pyautogui.screenshot()
    image.save("screenshotdsa.jpg")
    print("saved screenshot")

def webcampic():
    import cv2
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if ret:
        cv2.imwrite("campic2.jpg", frame)
        print("Saved web cam pic")
    else:
        print("Unable to access webcam")


def microphonecapture():
    # Audio settings
    seconds = 5  # Record Duration
    sample_rate = 44100  # Samples per second
    print("Recording ya twin...")
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until recording is finished
    write("Levi_record.wav", sample_rate, audio)
    print("Saved recording...")


def menu():
    print("\n" + "=" * 200)
    banner1()
    print("=" * 200)
    print("1) Screenshot capture")
    print("2) Webcam photo capture")
    print("3) Record microphone audio")
    print("0) Exit")


def main():
    while True:
        menu()
        choice = input("Enter your option: ")
        if choice == "1":
            # print("call screenshot capture")
            screenshotcapture()
        elif choice == "2":
            # print("call webcam photo capture")
            webcampic()
        elif choice == "3":
            # print("call record microphone audio")
            microphonecapture()
        elif choice == "0":
            print("Thank you for using this program, Good bye!")
            break
        else:
            print("Invalid option, please try again")


main()


