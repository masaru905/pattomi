from flask import Flask, render_template, request
from model_sum import summarize_docx
from model_co import co_network
from model_cloud import word_cloud

app = Flask(__name__)

# indexページ
@app.route("/", method=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

# cloudページ 
@app.route("/result_cloud", methods=["GET", "POST"])
def upload_cloud():
    if request.method == "GET":
        return render_template('result_cloud.html')
    elif request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            sum_result = summarize_docx(file)
            cloud = word_cloud(file)
            return render_template('result_cloud.html', sum_result=sum_result)
        else:
            error_message = "エラーが発生しました。Wordファイルを送信して下さい。"
            return render_template('result_cloud.html', error_message=error_message)

# networkページ
@app.route("/result_co", methods=["GET", "POST"])
def upload_co():
    if request.method == "GET":
        return render_template('result_co.html')
    elif request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            sum_result = summarize_docx(file)
            co_net = co_network(file)
            return render_template('result_co.html', sum_result=sum_result)
        else:
            error_message = "エラーが発生しました。Wordファイルを送信して下さい。"
            return render_template('result_co.html', error_message=error_message)
    
# ファイルの適合確認
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'docx'
    
if __name__ == "__main__":
    app.run(debug=True)