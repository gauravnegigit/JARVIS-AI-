import datetime
import pyttsx3
import wikipedia 
import speech_recognition as sr 
import webbrowser
import os 
import random

# importing modules for sending email with attachment 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[0].id)

def speak(text):
    print(text + '\n\n')
    engine.say(text)
    engine.runAndWait()

def send(to , content):
    server = smtplib.SMTP('smtp.gmail.com' , 587)
    server.ehlo()
    server.starttls()
    server.login('' , 'password')     # the password must be taken by the user by readung it from another file for security purposes 
    server.sendemail('' , to , content)
    server.close() 

def sendAttachment(to , content):
    """
    This function will come in handy in sending the video as an attachment to the required gmail account 
    """

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    msg['From'] = 'sender_email_id'
      
    # storing the receivers email address 
    msg['To'] = to 

    sender  , receiver = 'sender_email_id' , to 
      
    # storing the subject 
    msg['Subject'] = "Security camera"

    # attaching the body within the msg instance 
    msg.attach(MIMEText("" , 'plain'))

    speak("Please enter the file's location ...")
    loc = input()

    run = True 
    while run : 
        try : 
            attachment = open(loc , 'rb')
            run = False 
        except :
            speak('Please enter valid location ')

    speak("Please enter the filename ...")
    filename = input()

    p = MIMEBase('application' , 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition' , f"attachement; filename = {filename}")

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com' , 587)

    # start TLS for security
    s.starttls()
      
    # Authentication
    s.login(sender, "password")  # the password must be taken by the user by readung it from another file for security purposes 
      
    # Converts the Multipart msg into a string
    text = msg.as_string()
      
    # sending the mail
    s.sendmail(sender , receiver, text)
      
    # terminating the session
    s.quit()


def wish():
    hour = datetime.datetime.now().hour 
    if hour >= 0 and hour > 12 :
        speak("Good morning sir !")
    elif hour >= 12 and hour <= 18 :
        speak("Good afternoon sir !")
    else :
        speak("Good evening sir !")
    
    speak("I am Jarvis sir , Please tell me how may I help you .")

def takeCommand():
    """
    IT TAKESS MIRCOPHONE INPUT FROM TEH USER AND RETURNS STRING OUTPUT 
    """

    r = sr.Recognizer()
    with sr.Microphone() as source :
        print("Listening ....")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try :
        print("Recognizing ...")
        query = r.recognize_google(audio , language = 'en-in')
        print(f'User said {query}\n')
    
    except Exception as e :
        print("Say again please ...")
        return "None"
    
    return query 


def main():
    """
    this function handles the full functionality of jarvis 
    """

    wish()

    # logic for performing all the tasks from jarvis 
    while True :
        query = takeCommand().lower()

        if 'wikipedia' in query :
            speak('Searching Wikipedia ...')
            query = query.replace("wikipedia" , "")
            results = wikipedia.summary(query , sentences = 4)
            speak(f"\n\nAccording to wikipedia {results}")
        
        elif 'open youtube' in query :
            webbrowser.open('youtube.com')
        
        elif 'open google' in query :
            webbrowser.open('google.com')
        
        elif 'open stackoverflow' in query :
            webbrowser.open('stackoverflow.com')
        
        elif 'open website' in query :
            speak("Please enter the website ... \n")
            website = input()

            while True :
                try :
                    webbrowser.open(website)
                    break 
                except :
                    speak("PLEASE ENTER THE VALID WEBSITE ....")
        
        elif 'play music' in query :
            music_dir = ''
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir , songs[random.randint(0 , len(songs) - 1)]))

        elif "time" in query :
            stime= datetime.datetime.now().strftime("%H%M%S")
            speak(f"Sir , the time is {stime}")

        elif 'open code' in query :
            dir = r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(dir)
        
        elif "open" in query and "file" in query :
            dir = input("Please enter the file's location ...")

            run = True 
            
            while run : 
                try :
                    os.startfile(dir)
                    run = False 

                except Exception as e :
                    speak("Please try again ...")
            
        elif "send email" in query :
            send_dict = {"gaurav" : "id" , "xyz" : "id"}   # this dictionary must conatin the username as teh key and the id as the value 

            for key in send_dict :
                if key in query :
                    to = send_dict[key]

            try :
                speak("What should I send ? ")
                content = takeCommand()

                speak("Need to send some attached files as well ?")
                answer = input()


                if answer : 
                    sendAttachment(to,content)
                else :
                    send(to , content)
            
            except :
                speak("Sorry unable to send the email")
        
        elif 'quit' in query :
            quit()

if __name__ == '__main__':
    main()