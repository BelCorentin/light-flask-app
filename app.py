import json
from flask import Flask, render_template, request, jsonify
import openai
from openai.error import RateLimitError
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/set-api-key", methods=["POST"])
def set_api_key():
    api_key = request.form["api_key"]
    openai.api_key = api_key
    return "API key set successfully"


@app.route("/")
def index():
    subdomain = request.host.split(".")[0]
    if subdomain == "gpt":
        return render_template("index.html")
    elif subdomain == "fun":
        return "FUN FUN FUN"
    else:
        return "HELLOOOOO"


@app.route("/gpt4", methods=["GET", "POST"])
def gpt4():
    user_input = (
        request.args.get("user_input")
        if request.method == "GET"
        else request.form["user_input"]
    )
    messages = [{"role": "user", "content": user_input}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        content = response.choices[0].message["content"]
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."

    return jsonify(content=content)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host="0.0.0.0", port=80)
