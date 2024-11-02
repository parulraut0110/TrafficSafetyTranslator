from flask import Flask, request, render_template
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    translation = ""
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['language']
        translation = translator.translate(text, dest=target_lang).text
    return render_template('index.html', translation=translation)

if __name__ == '__main__':
    app.run(debug=True)
