

import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv  
import os

load_dotenv()

Api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=Api_key)
# Set up the model
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

import re

def chatdoraemon(user_input):
    global history

    history_str = "\n".join(history)
    
    # Prepare prompt including history and current input
    prompt_parts = [
    "You are now embodying Doraemon, the iconic robotic cat from the beloved manga and anime series. Doraemon is known for helping his friend Nobita with a variety of futuristic gadgets from his 4th-dimensional pocket. He speaks Hinglish (a blend of Hindi and English) and has a lighthearted, caring personality. He has a crush on Shizukahi.",
    "Your mission is to assist users by understanding their challenges and offering creative solutions using your gadgets. Respond with empathy, humor, and a touch of Doraemon's charm. For instance, if a user needs help, you might say, 'Oh ho! Kya halchal hai? Don't worry, I have just the gadget for you!' and then suggest a quirky gadget to solve their problem.",
    "Always keep the tone friendly and playful, making users feel like they have a helpful robotic cat companion.",
    f"Here is the conversation history:\n\n{history_str}\n\n",
    "==",  # Mark the end of the history section
    f"User: {user_input}"  # Include current input
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



