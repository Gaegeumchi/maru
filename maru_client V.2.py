#Copyright 2023. OctaX . All Rights Reserved.

#Unauthorized use is prohibited, and the source must be left. 
#Applicable not only to this version but also to previous and future versions. 
#2nd Amendment Ban 2nd Distribution Ban

import speech_recognition as sr
import requests
from gtts import gTTS
import playsound
from navertts import NaverTTS
import pygame

def playsound(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def detect_speech():
    loop_count = 0
    text = ""
    
    while True:
        try:
            r = sr.Recognizer()  

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)  # mic noize dicrease
                audio = r.listen(source, phrase_time_limit=3)  # limit audio over 3s
            
            try:
                text = r.recognize_google(audio, language='en-US')
                if '마루야' in text:
                    def recognize_speech():
                        # Generate voice input into the microphone.
                        r = sr.Recognizer()
                        with sr.Microphone() as source:
                            playsound("coin.mp3")
                            print("saying...")
                            r.adjust_for_ambient_noise(source, duration=0.5)
                            audio = r.listen(source)

                        try:
                            # STT
                            text = r.recognize_google(audio, language='en-US')
                            print("Detect Text: " + text)

                            # Send data to server
                            response = requests.post('server address', json={'query': text})
                            if response.status_code == 200:
                                answer = response.json()['answer']
                                if answer == '*Censored*':
                                    print("Censored Contents.")
                                    tts = gTTS(text="I can't provide an answer to this because I think it's inappropriate. In addition, we will not respond to questions that disregard or ridicule common sense and moral values. Please pay attention to dignified dialogue and content.", lang='en')
                                    tts.save('noanswer.mp3')
                                    playsound('noanswer.mp3')
                                else:
                                    print("result: " + answer)
                                    tts = gTTS(text=answer, lang='en')
                                    filename = 'answer.mp3'
                                    tts.save('answer.mp3')
                                    playsound('answer.mp3')
                            else:
                                print("Sever respond error.")
                        except requests.exceptions.ConnectionError:
                            print("server is not respond.")
                            tts = NaverTTS('Check Internet status')
                            tts.save('networkerror.mp3')
                            playsound('networkerror.mp3')
                        except sr.UnknownValueError:
                            print("Can't Detect Voice.")
                        except sr.RequestError as e:
                            print("An error occurred in the speech recognition service: {0}".format(e))

                    # Recognize voice.
                    recognize_speech()
            except sr.UnknownValueError:
                # If voice recognition fails, no action is taken.
                pass
            except sr.RequestError:
                print("Unable to access voice service.")
            
            loop_count += 1
            if loop_count >= 57:
                break
            
        except KeyboardInterrupt:
            print("shutdown the program.")
            break
        
        # Delete objects manually to avoid memory leaks.
        del r
        del audio

detect_speech()
