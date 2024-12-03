from flask import Flask, render_template, request
from google.cloud import aiplatform

app = Flask(__name__)

def get_response(prompt):
    endpoint = aiplatform.Endpoint(endpoint_name="your_endpoint_name")
    response = endpoint.predict(instances=[{"text": prompt}])
    return response.predictions[0]["text"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
        return render_template("index.html", response=response)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)