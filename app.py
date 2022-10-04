from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data_entry")
def data_entry():
    return render_template('data_entry.html')
