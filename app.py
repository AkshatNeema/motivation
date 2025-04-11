from flask import Flask, render_template
import random

app = Flask(__name__)

quotes = [
    "Believe in yourself and all that you are.",
    "The future depends on what you do today.",
    "Push yourself, because no one else is going to do it for you.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Your limitation—it’s only your imagination.",
    "Dream it. Wish it. Do it.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones."
]

@app.route('/')
def home():
    quote = random.choice(quotes)
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    app.run(debug=True)
