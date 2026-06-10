
import speech_recognition as sr
import webbrowser
import musiclibrary
import requests
import pyttsx3 
from deep_translator import GoogleTranslator


r=sr.Recognizer()
OPENROUTER_API_KEY="ai_api_key"

newsapi="your_api_key"
def speak(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # 1. Automatically check if the text contains Hindi alphabet letters
        is_hindi = any('\u0900' <= char <= '\u097F' for char in text)
        
        # 2. Select the voice using your exact system indexes
        if is_hindi and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Index 1 is Kalpana
        else:
            engine.setProperty('voice', voices[0].id)  # Index 0 is Zira
            
        engine.setProperty('rate', 175)  # Set a clean, natural reading pace
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Offline Speech Engine Error: {e}")



def aiprocess(command):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
  
    headers={
    "Authorization": (f"Bearer {OPENROUTER_API_KEY}"),
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:ffhffff", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "Local Debug Script", # Optional. Site title for rankings on openrouter.ai.
    },
    json=({
    "model": "openrouter/free",
    "messages": [
      {
        "role": "system", 
        "content": "You are a helpful assistant. Crucial: Always reply in the exact same language or script used by the user. If the user asks in Hindi, reply in Hindi script. If they ask in English, reply in English."
      },
       {
                "role": "user",
                "content": command  # <-- ADD THIS: Passes your spoken question to the AI
            }
    ]
    })
    )

    return response.json()["choices"][0]["message"]["content"]




def process(c):
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        lists=c.lower().split(" ")
        if len(lists) > 1:
            songs=lists[1]
            if songs in musiclibrary.music:
                song=c.lower().split(" ")[1]
                link=musiclibrary.music[song]
                webbrowser.open(link)
    elif "news" in c or "समाचार" in c or "खबर" in c:
        # 1. Automatically detect which language the user used to ask for news
        # If Hindi characters are detected in your voice command, use Hindi, otherwise English
        user_lang = 'hi' if any('\u0900' <= char <= '\u097F' for char in c) else 'en'
        base_url = "https://newsapi.org/v2/top-headlines"
        query_parameters = {
            "q": "India",       # Searches for any active news containing "India"
            "pageSize": 3,
            "language":  user_lang,
            "apiKey": newsapi  
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
        try:
            
            response = requests.get(base_url, params=query_parameters,headers=headers)
            if "application/json" in response.headers.get("Content-Type", ""):
                news = response.json()
                if response.status_code == 200:
                    title_banner="--- आज की मुख्य समाचार ---" if user_lang == 'hi' else "--- Top Indian Headlines ---"
                    print(f"\n{title_banner}")
                    articles = news.get("articles", [])    
                    if not articles:
                        print("General news empty, pulling technology sector updates...")
                        speak("कोई समाचार नहीं मिला" if user_lang == 'hi' else "No news found.")
                    else:    
                        for article in articles:  # Top 3 headlines
                            original_title = article.get("title")
                            if not original_title or "Removed" in original_title:
                                continue
                            try:
                                translated_title = GoogleTranslator(source='auto', target=user_lang).translate(original_title)
                                print(f"{'समाचार' if user_lang == 'hi' else 'News'}: {translated_title}")
                                speak(translated_title)
                            except Exception as translate_error:
                                print(f"Original: {original_title}")
                                speak(original_title)
            
                else: 
                    print(f"NewsAPI Error: Status {response.status_code}")
                    print("Reason:", news.get("message", "Unknown error"))
            else:
                print("Error: Received HTML instead of JSON data.")
                
        except Exception as request_error:
            print(f"Network Connection Error: {request_error}")

    else:
        #Openai handel the request
        output=aiprocess(c)
        print(output)
        speak(output)


if __name__=="__main__":
    speak("Initializing meow.....")
    print("Initializing meow.....")
    while True:
        
        
    #listen for wake word "meow"
    #obtain speaker's words from microphone   
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                    print("Audio captured")
                    print("Recognizing...")
                try:
                    word = r.recognize_google(audio, language="en-IN").lower()
                    print(f"Heared:{word}")
                except:
                    word = r.recognize_google(audio, language="hi-IN").lower()
                    print(f"maine suna:{word}")
                if "meow" in word:
                    #listen for command
                    print("yes")
                    speak("yes") # Instant: plays a local file immediately

                    with sr.Microphone() as source:
                        print("Meow is active")
                        audio=r.listen(source,timeout=10,phrase_time_limit=5)
                        command=r.recognize_google(audio, language="hi-IN, en-IN").lower()
                        process(command)

            except Exception as e:
                print(" error; {0}".format(e))  



