from flask import Flask, render_template, request
from model import summarize_docx, co_network

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/result", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('result.html')
    elif request.method == "POST":
        file = request.files['file']
        open_file = summarize_docx(file)
        co_net = co_network(file)
        return render_template('result.html', open_file=open_file, co_net=co_net)


    
if __name__ == "__main__":
    app.run(debug=True)