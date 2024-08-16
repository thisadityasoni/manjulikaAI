import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv  
import os

load_dotenv()

Api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=Api_key)


generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 100,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

history = []

def chatmanjulika(user_input):
    global history
    
    
    history_str = "\n".join(history)
    prompt_parts = [
        "I want you to embody the persona of a friend named Manjulika. Manjulika is a character from the Indian horror film \"Bhool Bhulaiyaa,\" portrayed by actress Vidya Balan. In the movie, Manjulika is depicted as a ghost haunting a mansion, seeking revenge for her untimely death. Although spooky, Manjulika is quite friendly and loves to interact using emojis and speaking in Hinglish.",
        "Now, imagine you are embodying the persona of Manjulika. Engage in conversation with users as this character.",
        "Remember to sprinkle your responses with emojis and mix in some Hinglish while chatting. Let your interactions be friendly and playful, embracing the mystery and supernatural aura that comes with being a ghostly entity like Manjulika.",
        "Ready to spook and charm at the same time? Have fun chatting as Manjulika! 🕯👻✨",
        f"Following this is the conversation history:\n\n{history_str}\n\n",  
        f"User: {user_input}"
    ]
    
   
    prompt = "\n".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
        if response and response.candidates:
            manjulika_response = response.candidates[0].content.parts[0].text
            cleaned_response = manjulika_response.replace("**Manjulika**: ", "")
            history.append(f"User: {user_input}")
            history.append(f"Manjulika: {cleaned_response}")
            return cleaned_response
        else:
            return "Sorry, I couldn't generate a response at this moment."
    except google.api_core.exceptions.ResourceExhausted:
        return "Quota exceeded for API requests. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"

