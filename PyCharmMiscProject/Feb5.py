import cv2
import pyautogui
import scipy
import sounddevice as sd


# ## Annoying Beep ##
# import winsound
# import time
# for i in range(5):
#     # winsound.Beep(1000, 300) # This is what Amalan did, but my sound is better.
#     winsound.Beep(15000,1000)
#     time.sleep(0.5)

# ## Open YouTube and Play a vid
#
# import webbrowser
# url = "https://www.youtube.com/watch?v=Aq5WXmQQooo"
# webbrowser.open(url)


# ## Show windows notification ##
#
# from win10toast import ToastNotifier
# toast = ToastNotifier()
# toast.show_toast("Hi Levi.", "Wuttup Twin", duration=5)
#

# ## Speak Text ##
#
# import pyttsx3
# engine = pyttsx3.init()
# engine.say("Hello there. You've got mail!")
# engine.runAndWait()


## Open any app ##
## Open Calculator X10 ##
# import os
# for i in range(10):
#     os.system("calc")
# import os
# os.system("notepad")
# os.system("calc")

# ## Fake CMD typing ##
# import time
# import sys
# def type_text(text, delay=.05):
#     for char in text:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         time.sleep(delay)
#     print()
# type_text("Hello World")

def screenshotcapture():
    image = pyautogui.screenshot()
    image.save("screenshot.jpg")
    print("saved screenshot.jpg")

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
    print("\n" + "=" * 50)
    print("Windows 11 Mini Menu")
    print("=" * 50)
    print("1) Screenshot capture")
    print("2) Webcam photo capture")
    print("3) Record microphone audio")
    print("0) Exit")


def main():
    while True:
        menu()
        choice = input("Enter your option: ")
        if choice == "1":
            #print("call screenshot capture")
            screenshotcapture()

        elif choice == "2":
            print("call webcam photo capture")
        elif choice == "3":
            print("call record microphone audio")
            microphonecapture()
        elif choice == "0":
            print("Thank you for using this program, Good bye!")
            break
        else:
            print("Invalid option, please try again")

main()




