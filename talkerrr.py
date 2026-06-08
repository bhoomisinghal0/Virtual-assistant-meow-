import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
import requests
import json
from deep_translator import GoogleTranslator


r=sr.Recognizer()
OPENROUTER_API_KEY="ai_api_key"
newsapi="your_api_key"
def speak(text):
    engine=pyttsx3.init()
    engine.setProperty('voice', 'sapi5')
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiprocess(command):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
  
    headers={
    "Authorization": (f"Bearer {OPENROUTER_API_KEY}"),
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000", # Optional. Site URL for rankings on openrouter.ai.
    "X-OpenRouter-Title": "Local Debug Script", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
    "model": "openrouter/free",
    "messages": [
      {
        "role": "user",
        "content": command
      }
    ]
    })
    )

    return (response.json()["choices"][0]["message"]["content"])




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
    elif "news" in c:
        # FIX: Added the correct API endpoint path
        base_url = "https://newsapi.org/v2/top-headlines"
        query_parameters = {
            "q": "India",       # Searches for any active news containing "India"
            "pageSize": 3,
            "language": "hi",    
            "apiKey": newsapi  
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
        try:
            
            response = requests.get(base_url, params=query_parameters,headers=headers)
            if "application/json" in response.headers.get("Content-Type", ""):
                news = response.json()
                if response.status_code == 200:
                    print("\n--- आज की मुख्य समाचार (Indian News in Hindi) ---")
                    articles = news.get("articles", [])    
                    if not articles:
                        print("General news empty, pulling technology sector updates...")
                        query_parameters["category"] = "technology"
                        response = requests.get(base_url, params=query_parameters, headers=headers)
                        news = response.json()
                        articles = news.get("articles", [])
                    if not articles:
                        print("No news articles found right now across any major categories.")
                        speak("कोई समाचार नहीं मिला")
                    else:    
                        for article in articles:  # Top 3 headlines
                            original_title = article.get("title")
                            if not original_title or "Removed" in original_title:
                                continue
                            try:
                                translated_title = GoogleTranslator(source='auto', target='hi').translate(original_title)
                                print(f"समाचार: {translated_title}")
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
                word=r.recognize_google(audio).lower()
                print("Heard:", word)
                if "meow" in word:
                    #listen for command
                    print("yes")
                    speak("yes")
                    with sr.Microphone() as source:
                        print("Meow is active")
                        audio=r.listen(source,timeout=10,phrase_time_limit=5)
                        command=r.recognize_google(audio).lower()
                        process(command)

            except Exception as e:
                print(" error; {0}".format(e))  



