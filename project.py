import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import webbrowser
import time
import pyjokes

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print("Leo:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
    except:
        speak("Sorry, I couldn't understand.")
        return ""
    return command

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def tell_date_and_day():
    today = datetime.datetime.now()
    date = today.strftime("%B %d, %Y")
    day = today.strftime("%A")
    speak(f"Today is {day}, {date}.")

def tell_weather(city):
    api_key = "d1499c050613fd3cd51548d7caa46096"  
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] != "404":
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The weather in {city} is {desc} with {temp} degrees Celsius.")
        else:
            speak("City not found.")
    except:
        speak("Weather information is not available right now.")

def tell_news():
    api_key = "9981a56424184755b105267fb6910d0c"  
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}&pageSize=5"
    try:
        response = requests.get(url).json()
        articles = response["articles"]
        speak("Here are the top headlines:")
        for i, article in enumerate(articles[:5]):
            speak(f"{i+1}. {article['title']}")
    except:
        speak("Sorry, I couldn't fetch the news right now.")

def open_website(site_name):
    websites = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'chatgpt': 'https://chat.openai.com',
        'spotify': 'https://open.spotify.com'
    }
    if site_name in websites:
        speak(f"Opening {site_name}")
        webbrowser.open(websites[site_name])
    else:
        speak("I can't find that website.")

def answer_why_question(question):
    topic = question.replace("why", "").strip()
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(f"Here's why: {result}")
    except:
        speak(f"There are many reasons why {topic} is important.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def search_google(command):
    search_term = command.replace("search", "").strip()
    if search_term:
        speak(f"Searching for {search_term}")
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
    else:
        speak("What should I search for?")

def run_assistant():
    speak("Hello! I'm Leo, your virtual assistant.")
    speak("What is your name?")
    user_name = listen()

    if user_name:
        speak(f"Nice to meet you, {user_name}. How can I help you?")

    while True:
        command = listen()

        if 'play' in command:
            song = command.replace('play', '').strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif 'time' in command:
            tell_time()

        elif 'date' in command or 'day' in command:
            tell_date_and_day()

        elif 'weather in' in command:
            city = command.split('weather in')[-1].strip()
            tell_weather(city)

        elif 'news' in command:
            tell_news()

        elif 'who is' in command or 'what is' in command or 'tell me about' in command:
            topic = command.replace('who is', '').replace('what is', '').replace('tell me about', '').strip()
            try:
                info = wikipedia.summary(topic, sentences=2)
                speak(info)
            except:
                speak("Sorry, I couldn't find that.")

        elif 'why' in command:
            answer_why_question(command)

        elif 'open google' in command:
            open_website('google')

        elif 'open youtube' in command:
            open_website('youtube')

        elif 'open chatgpt' in command:
            open_website('chatgpt')

        elif 'open spotify' in command:
            open_website('spotify')

        elif 'tell me a joke' in command:
            tell_joke()

        elif 'search' in command:
            search_google(command)

        elif 'thank you' in command or 'thanks' in command:
            speak("You're welcome!")

        elif 'exit' in command or 'stop' in command:
            speak(f"Goodbye {user_name}! Leo signing off.")
            break

        elif command:
            speak("Sorry, I didn't get that.")
run_assistant()
