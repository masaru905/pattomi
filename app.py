from flask import Flask, render_template, request
from model_sum import summarize_docx
from model_co import co_network
from model_cloud import word_cloud

app = Flask(__name__)

# indexページ
@app.route("/")
def index():
    return render_template('index.html')

# cloudページ 
@app.route("/result_cloud", methods=["GET", "POST"])
def upload_cloud():
    if request.method == "GET":
        return render_template('result_cloud.html')
    elif request.method == "POST":
        file = request.files['file']
        sum_result = summarize_docx(file)
        cloud = word_cloud(file)
        return render_template('result_cloud.html', sum_result=sum_result)

# networkページ
@app.route("/result_co", methods=["GET", "POST"])
def upload_co():
    if request.method == "GET":
        return render_template('result_co.html')
    elif request.method == "POST":
        file = request.files['file']
        sum_result = summarize_docx(file)
        co_net = co_network(file)
        return render_template('result_co.html', sum_result=sum_result)
    
if __name__ == "__main__":
    app.run(debug=True)