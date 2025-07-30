import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import pyjokes
import os
import smtplib
import pyautogui
import time
import threading
import random
from win10toast import ToastNotifier
import win32gui
import pywhatkit

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate
engine.setProperty('volume', 1.0)  # Set volume level (0.0 to 1.0)
tts_lock = threading.Lock()  # Lock object for thread-safe TTS

notifier = ToastNotifier()

# Speak function
def speak(text):
          # Ensure thread-safe access to TTS
        engine.say(text)
        engine.runAndWait()

# Check WhatsApp notification
def check_whatsapp_notification():
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    left = int(width * 0.85)
    top = int(height * 0.1)
    right = width
    bottom = int(height * 0.9)
    cropped = screenshot.crop((left, top, right, bottom))

    colors = cropped.getcolors(maxcolors=100000)
    if colors:
        for count, color in colors:
            r, g, b = color[:3]
            if g > r and g > b and g > 200:
                speak("You have a new WhatsApp message.")
                break

# Email function
def send_email(to, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail('your_email@gmail.com', to, message)
        server.quit()
        speak("Email sent successfully")
    except Exception as e:
        speak("Sorry, I couldn't send the email")
        print(e)

# Notification listener
def notification_listener():
    def get_active_window_title():
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

    last_title = ""
    while True:
        current_title = get_active_window_title()
        if current_title != last_title and current_title != "":
            last_title = current_title
            speak(f"New notification or window from {current_title}")
        time.sleep(5)

# Extra notification watcher for WhatsApp

def notification_watcher():
    while True:
        check_whatsapp_notification()
        time.sleep(15)

# Main command processor
def process_command(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "what is the time" in command or "what time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "send email" in command:
        speak("To whom?")
        to = input("Enter recipient email: ")
        speak("What is the subject?")
        subject = input("Subject: ")
        speak("What should I say?")
        body = input("Body: ")
        send_email(to, subject, body)

    elif "send whatsapp message" in command or "send message" in command:
        speak("Enter number in international format")
        number = input("Enter WhatsApp Number: ")
        speak("What should I say?")
        msg = input("Enter message: ")
        pywhatkit.sendwhatmsg_instantly(number, msg, wait_time=10)
        speak("Message sent on WhatsApp")

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    check_whatsapp_notification()

# Voice assistant logic

def run_assistant():
    speak("Hello, I am Tom. How can I help you today?")
    threading.Thread(target=notification_listener, daemon=True).start()
    threading.Thread(target=notification_watcher, daemon=True).start()
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if command.lower() == "tom":
                speak("Yes sir, how can I help you?")
                continue
            else:
                process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")

        except sr.RequestError as e:
            print(f"Request error: {e}")
            speak("Speech service is not available.")

        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("Something went wrong.")

# Start the assistant
if __name__ == "__main__":
    run_assistant()
