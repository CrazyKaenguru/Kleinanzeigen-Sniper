"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyAy4nbD6gOXpam0Gk5FlEIZo7Ziu5Kp0ME")

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  
)

chat_session = model.start_chat(
  history=[
    
  ]
)

response = chat_session.send_message("""Verhalte dich wie ein programm, dass entscheidet ob die nachfolgenden informationen über ein angebot den folgenden anforderungen entsprechen. wenn ja, dann antworte mit 1 wenn nicht, antworte mit 0 und ignoriere urls Anforderung: kein defekt vorliegend, wenige gebrauchsspuren,muss ein Iphone X sein, muss ein Angebot sein Informationen:




  "description": "\n                                Ich verkaufe hier die leere Originalverpackung eines iPhone 12 in Schwarz. Die Kartonbox ist neu und beinhaltet die originalen Apple Sticker sowie alle sonstigen Zubeh\u00f6rteile, die \u00fcblicherweise mit der Verpackung geliefert werden.Eigenschaften:Originalverpackung f\u00fcr iPhone 12Farbe: SchwarzZustand: Neu und unbenutztLieferumfang: Kartonbox, Apple Sticker, sonstige originale Zubeh\u00f6rteile (ohne Handy und Ladekabel)Ideal f\u00fcr Sammler oder als Ersatz f\u00fcr verlorene Verpackungen. Bei Interesse oder Fragen einfach melden!",
        "price": 9,
        "vb": false,
        "name": "2x iPhone 12 Black 128GB 5G Karton Box NEU Apple Sticker"





























 , triff nur eindeutige entscheidungen und antworte nur mit 0 wenn ersichtlich ist, dass die anforderungen nicht erfüllt wurden. Wenn keine expliziten angaben gemacht werden antworte mit 1""")

print(response.text)