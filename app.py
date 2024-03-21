from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

