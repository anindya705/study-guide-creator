from flask import Flask, render_template
from pathlib import Path
from summarizer import summarize

app = Flask(__name__)

@app.route("/")
def index():
    txt = Path('articles/articles.txt').read_text()
    txt = txt.replace('\n', '')
    return render_template('index.html', output = summarize(txt, 3), org = txt)
