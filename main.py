import speech_recognition as sr
import google.generativeai as genai
import pygame
import pyttsx3
import webbrowser
import music
#
recognizer = sr.Recognizer()
pygame.mixer.init()
pygame.mixer.music.load("MIRA/main/ding-36029.mp3") 
pygame.mixer.music.set_volume(0.5)   
genai.configure(api_key=music.apikey)
model = genai.GenerativeModel('gemini-1.5-flash')

def speak(text):
    print("MIRA:", text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processCommand(text):
    if "open google" in text.lower():
        speak("opening google")
        webbrowser.open("https://google.com")
    elif "open youtube" in text.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
    elif "open news" in text.lower():
        speak("opening news")
        webbrowser.open("https://google.com/news")    
    elif text.lower().startswith("play"):
        play=""
        for song in music.music:
            if song in text.lower():
                play=song
        if play!="": 
          speak(f"playing {play}")       
          webbrowser.open(music.music[play])
        else:
            speak("No song found")  
    else:
       try:   
        response=model.generate_content(text)
        speak(response.text)
       except Exception as e:
           print(f"{e} error with gemini") 


if __name__ == "__main__":
    speak("Initializing MIRA...")



while True:
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)
            pygame.mixer.music.play()
        vo = recognizer.recognize_google(audio)  
        print("You said:", vo)
        if "bye-bye" == vo.lower():
            speak("Goodbye!")
            break
        
        if vo.strip():  
            processCommand(vo)
        else:
            speak("I heard silence.")

    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")

    except sr.RequestError as e:
        print("Recognition error:", e)
        speak("Recognition service is unavailable.")
    except sr.WaitTimeoutError:  
        print("No speech detected, retrying...")
        continue 