# ## Take a webcam photo ##

import cv2
cam = cv2.VideoCapture(0)

ret, frame = cam.read()

cam.release()

if ret:
    cv2.imwrite("campic.jpg", frame)
    print("Saved levi web cam pic")
else:
    print("Unable to access webcam")




## Take a Screenshot ##

# import pyautogui
# image = pyautogui.screenshot()
# image.save("screenshot.jpg")
# print("saved screenshot.jpg")

# ## Record Microphone Audio ##
import scipy
import sounddevice as sd
from scipy.io.wavfile import write

# Audio settings
seconds = 5 # Record Duration
sample_rate = 44100 # Samples per second
print("Recording ya twin...")

audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
sd.wait() # Wait until recording is finished

write("Levi_record.wav", sample_rate, audio)
print("Saved recording...")

# ## Show windows event log ##
# import os
# os.system('powershell "Get-EventLog -LogName System -Newest 20 | Format-Table -AutoSize"')
#


