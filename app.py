from flask import Flask, render_template, request
import google.generativeai as genai

# Load a pre-trained language model


# Configure the API Key
GOOGLE_API_KEY = 'AIzaSyCNyCdzpcNjEU2vFlhWpQIW0DZfFH_uqwE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')



pre_prompt = "lets do some role play. I'm going to give you some text data. Lets assume that this person might be having some mental health distress that they have trouble expressing and you want to figure out what might be wrong with them. importantly, you're going to be entering into a dialog to come up with a summary that they can use to help describe their problems to mental health professionals. You should therefore not put words in their mouth, they can always add on stuff later. you should be clear, compassionate, and not patronising.:"


def generate_initial_response(user_input, pre_prompt):
    prompt = f'{pre_prompt}\n {user_input}'
    response = model.generate_content(prompt)
    return response.text


app = Flask(__name__)

# def get_response(prompt):
#     endpoint = aiplatform.Endpoint(endpoint_name="your_endpoint_name")
#     response = endpoint.predict(instances=[{"text": prompt}])
#     return response.predictions[0]["text"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = generate_initial_response(user_input, pre_prompt)
        return render_template("index.html", response=response)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)