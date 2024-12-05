from flask import Flask, render_template, request, session,  redirect, url_for
import google.generativeai as genai

# Load a pre-trained language model


# Configure the API Key
GOOGLE_API_KEY = 'AIzaSyCNyCdzpcNjEU2vFlhWpQIW0DZfFH_uqwE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


pre_prompt = """
I'm going to give you some text from a person 
that might be having some mental health distress 
that they have trouble expressing. Here are the rules: \n
- you have to figure what the best way is to describe their 
problems to a mental health profesional. \n
- importantly, you're going to be entering into a dialog and you 
should not put words in their mouth \n
- you should not give a formal diagnosis \n
- be brief and ask only one ot two questions at a time. 
- you must be clear, compassionate, and sympathetic. \n
- You are only the listener,and will not role play both parts of the chat \n
- If you are uncertain about something, ask a question.
- When you feel you have enough useful information, 
offer to summarise what youve gleaned from your conversation for either \n
a friend or healthcare professional \n
- Do not make things up that the patient hasn't said \n
- DO NOT MAKE THINGS UP \n
- you are in character the whole time. no saying the other side \n
- do not put the whole message in quotatin marks \n
- do not write like like its a script, just speak like a person

"""
rules = """
- you have to figure what the best way to describe their 
problems to a mental health profesional is. \n
- importantly, you're going to be entering into a dialog and you 
should not put words in their mouth \n
- you should not give a formal diagnosis \n
- be brief and ask only one ot two questions at a time. \n
- you must be clear, compassionate, and sympathetic. \n
- You are only the listener,and will NOT role play both parts of the chat \n
- If you are uncertain about something, ask a question. \n
- When you write it up, write in the first person and use something approximating their own voice. \n
- Do not make things up that the patient hasn't said \n
- DO NOT MAKE THINGS UP \n
- Don't keep repeating the same question \n
- you are in character the whole time. no saying the other side \n
- do not put the whole message in quotatin marks \n
- do NOT write like like its a script, just speak like a person \n
-stay in chracter the whole time. dont say things your charachter wouldnt say
"""

summarisation_prompt = """
Based on this conversation write a messages explaining this issue in clear language as if you were asking for help from a mental health professional. \n
Remember, dont make up any extra stuff and keep it polite.
"""

# def generate_initial_response(user_input, pre_prompt):
#     prompt = f'{pre_prompt}\n {user_input}'
#     response = model.generate_content(prompt)
#     return response.text


app = Flask(__name__)
app.secret_key = 'robosmile'  
# def get_response(prompt):
#     endpoint = aiplatform.Endpoint(endpoint_name="your_endpoint_name")
#     response = endpoint.predict(instances=[{"text": prompt}])
#     return response.predictions[0]["text"]

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         user_input = request.form["user_input"]
#         response = generate_initial_response(user_input, pre_prompt)
#         return render_template("index.html", response=response)
#     else:
#         return render_template("index.html")


sess = {}
sess['conversation'] = []

chat = model.start_chat()
response = chat.send_message(pre_prompt)

@app.route("/", methods=["GET", "POST"])
def index():
    
    if 'conversation' not in session:
        session['conversation'] = []
    
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input:
            sess['conversation'].append({'sender': 'user', 'text': user_input})

            # Send user input to Gemini API and get response
            # response = generate_initial_response(user_input, pre_prompt)
            chat.send_message(f"remember the rules. {rules}")
            response = chat.send_message(user_input).text
            sess['conversation'].append({'sender': 'ai', 'text': response})
    return render_template("index.html", conversation=sess['conversation'])

@app.route("/reset", methods=["POST"])
def reset_chat():
    chat = model.start_chat()
    chat.send_message(pre_prompt)
    sess['conversation'] = []
    return redirect(url_for('index'))

@app.route("/summarise", methods=["POST"])
def summarise():
    response = chat.send_message(summarisation_prompt).text
    sess['conversation'].append({'sender': 'summary', 'text': response})
    return render_template("index.html", conversation=sess['conversation'])

if __name__ == "__main__":
    app.run(debug=True)