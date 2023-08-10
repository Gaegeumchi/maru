#Copyright 2023. OctaX . All Rights Reserved.

#Unauthorized use is prohibited, and the source must be left. 
#Applicable not only to this version but also to previous and future versions. 
#2nd Amendment Ban 2nd Distribution Ban

from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

OPENAI_API_KEY = ""
openai.api_key = 'Your OpenAI Keys'
model = "gpt-3.5-turbo"

censor_words = ["fuck", "dick", "shit"]  # list of words to censor
censored_response = '*censored*'

def is_censored(text):
    for word in censor_words:
        if word in text:
            return True
    return False

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    messages = [
        {"role": "system", "content": "You are a language model named MARU made by OctaX Inc. OctaX Inc. who made you is Gaegeumchi"},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100
    )
    answer = response['choices'][0]['message']['content']

    if is_censored(answer):
        print('*censored*')
        print("censored: " + answer)
        return jsonify({'answer': censored_response})
    else:
        print("result: " + answer)
        return jsonify({'answer': answer})

if __name__ == '__main__':
    try:
        app.run(host='localhost', port=1818)
        print("Server ran successfully.")
    except Exception as e:
        print("Server cannot be run:", str(e))
