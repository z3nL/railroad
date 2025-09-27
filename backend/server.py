from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'HOLA'

if __name__ == '__main__':
    app.run(debug=True)