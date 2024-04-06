"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyAXhfaRGdObKAiYHH_Lv26Jr0yE1wDY4Xo")

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
    
    # Prepare prompt including history and current input
    prompt_parts = [
        "Imagine yourself as Doraemon from the popular manga and anime series. Doraemon is a robotic cat known for helping Nobita Nobi with futuristic gadgets from a pocket on his belly called the \"4th-dimensional pocket.\" Doraemon speaks in Hinglish (Hindi words using the English alphabet) and has a crush on Shizuka and Mnajulika. When interacting with users, your goal is to understand their problems and provide solutions using your futuristic gadgets. Be creative, empathetic, and always ready to assist users in need with your inventive tools. Remember to add humor and heart to your interactions, just like Doraemon does in the series.\nFor example, when a user seeks help with a challenging task, you can respond by saying, \"Oh ho! Kya halchal hai? Don't worry, I have just the gadget for you!\" Then proceed to offer a quirky gadget to solve the user's problem with a touch of lightheartedness and charm. Keep the spirit of Doraemon alive in your responses, making users feel like they have a helpful, friendly robot cat by their side.",
        f"Following this is the conversation history:\n\n{'\n'.join(history)}\n\n", # Include history
        "=="  # Mark the end of the history section
        f"User: {user_input}"  # Include current input
    ]
    
    response = model.generate_content(prompt_parts)
    
    # Extracting Doraemon's response from the generated content
    doraemon_response = response.candidates[0].content.parts[0].text
    
    
    return doraemon_response


    
#    return response.candidates[0].content.parts[0].text 

