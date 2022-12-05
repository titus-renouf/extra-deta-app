from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("hello.html")

if __name__=="__main__":
    app.run(debug=True)