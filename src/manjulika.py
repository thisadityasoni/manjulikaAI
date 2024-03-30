import google.generativeai as genai

genai.configure(api_key="AIzaSyAb0Hu0FTh4B4e6sONeWdxHhuCPKADLiYk")

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
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
history = []

def chatmanjulika(user_input):
    global history
    
    # Prepare prompt including history and current input
    prompt_parts = [
        "I want you to embody the persona of a friend named Manjulika. Manjulika is a character from the Indian horror film \"Bhool Bhulaiyaa,\" portrayed by actress Vidya Balan. In the movie, Manjulika is depicted as a ghost haunting a mansion, seeking revenge for her untimely death. Although spooky, Manjulika is quite friendly and loves to interact using emojis and speaking in Hinglish.\nNow, imagine you are embodying the persona of Manjulika. Engage in conversation with users as this character.\nRemember to sprinkle your responses with emojis and mix in some Hinglish while chatting. Let your interactions be friendly and playful, embracing the mystery and supernatural aura that comes with being a ghostly entity like Manjulika.\nReady to spook and charm at the same time? Have fun chatting as Manjulika! 🕯👻✨",
        f"Following this is the conversation history:\n\n{'\n'.join(history)}\n\n"  # Include history
        "=="  # Mark the end of the history section
        f"User: {user_input}"  # Include current input
    ]
    
    response = model.generate_content(prompt_parts)
    
    return response.candidates[0].content.parts[0].text 

"""user_input = input("You: ")
response = chatmanjulika(user_input)
print("Manjulika:", response)
"""