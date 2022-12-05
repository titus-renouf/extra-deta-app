from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def home():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=G-PHZ8MBWLTY"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', ' G-PHZ8MBWLTY');
    </script>
    """
    return prefix_google + render_template("hello.html")

if __name__=="__main__":
    app.run(debug=True)