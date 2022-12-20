from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
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
    if request.method == 'POST':
        if request.form.get('action1') == 'Home':
            return prefix_google + render_template('home.html')

        elif request.form.get('action2') == 'About':
            return prefix_google + render_template('about.html')
        else:
            pass 
    elif request.method == 'GET':
        return prefix_google + render_template('hello.html')

    return prefix_google + render_template("hello.html")


@app.route('/logger', methods=['GET', 'POST'])
def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')

    return render_template('textbox.html')
    #deta logs in terminal to see back-end logs


@app.route('/reqGA')
def reqGA():
    req = requests.get("https://www.google.com/")
    app.logger.info(req)
    return req.cookies.get_dict()


@app.route('/myreqGA')
def myreqGA():
    req = requests.get('https://analytics.google.com/analytics/web/#/a250985568p345087452')
    app.logger.info(req)
    return req.text


if __name__=="__main__":
    app.run(debug=True)