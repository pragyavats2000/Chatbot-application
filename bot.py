import nltk
from nltk.chat.util import Chat, reflections
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('wordnet')
import sqlite3

try:
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Delete rows that match a pattern
    pattern_to_delete = 'some_pattern'
    c.execute("DELETE FROM pairs WHERE pattern=?", (pattern_to_delete,))  
    
    # Delete rows with a specific ID
    id_to_delete = 192
    c.execute("DELETE FROM pairs WHERE id=?", (id_to_delete,)) 
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
except Exception as e:
    print(e)

lemmatizer = WordNetLemmatizer()

# Fetch pairs from the database
pairs = []
try:
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    for row in c.execute('SELECT pattern, response FROM pairs').fetchall():
        pairs.append((r'{}'.format(row[0]), (row[1],)))
    conn.close()
except Exception as e:
   print(e)
# print(pairs)

# pairs = [
#     (r'what are *[a-z] here', ('Everything is there',),),
#     (r'hi', ('Nice', 'Well'),),
# ]
# lemmatized_pairs = pairs


# import re

# def wildcard_response(pattern, response, message):
#     match = re.search(pattern, message)
#     if match:
#         wildcards = match.groups()
#         for i, wildcard in enumerate(wildcards):
#             response = response.replace("%"+str(i+1), wildcard)
#         return response

lemmatized_pairs = []
for pattern, responses in pairs:
    tokenized_pattern = word_tokenize(pattern)
    lemmatized_pattern = ' '.join([lemmatizer.lemmatize(token.lower()) for token in tokenized_pattern])
    lemmatized_pairs.append([lemmatized_pattern, responses])

chatbot = Chat(lemmatized_pairs, reflections)

print("Welcome to our restaurant! How can I assist you today?")

from flask import Flask, render_template, request
import time
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('bot.html')

@app.route('/menu')
def menu():
    # Add your code to generate the menu page here
    return render_template('menu.html')

chat_log = []
@app.route('/chat', methods=['POST', 'GET'])
def get_chatbot_response():
    print('get_chatbot_response() called')  
    response = ''
    if request.method == 'POST':
        user_input = request.json['user_input']
        print(f'User input: {user_input}')  
        if user_input.lower() == 'quit':
            response = 'Goodbye! Thank you for visiting our restaurant.'
        else:
            response = chatbot.respond(user_input)
            print(f'Chatbot response: {response}')  
            if response == None:
                response = 'I am sorry, I don\'t know what you mean.'
                
        chat_log.append({'side': 'left', 'message': response})

        return response

if __name__ == '__main__':
    app.run(debug=True)


