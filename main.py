from pytrends.request import TrendReq
from flask import Flask, render_template, request
import requests
from datetime import datetime

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


@app.route('/pytrends')
def googletrendchart():
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=["Lionel Messi", "Cristiano Ronaldo"], timeframe='today 90-d', geo='FR')
    df = pytrends.interest_over_time()
    data_messi = df['Lionel Messi'].tolist()
    data_ronaldo = df['Cristiano Ronaldo'].tolist()
    data_date = df.index.values.tolist()
    timestamp_in_seconds = [element/1e9 for element in data_date]
    date = [datetime.fromtimestamp(element)for element in timestamp_in_seconds]
    days = [element.date() for element in date]
    months = [element.isoformat() for element in days]
    params = {
        "type": 'line',
        "data": {
            "labels": months,
            "datasets": [{
                "label": 'Lionel Messi',
                "data": data_messi,
                "borderColor": '#3e95cd',
                "fill": 'false',
            },
                {
                "label": 'Cristiano Ronaldo',
                "data": data_ronaldo,
                "borderColor": '#ffce56',
                "fill": 'false',
            }
            ]
        },
        "options": {
            "title": {
                # + str(topic_1) + " et " + str(topic_2)
                "text": 'Comparaison entre'
            },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": 'true'
                    }
                }]
            }
        }
    }

    prefix_chartjs = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
         <canvas id="myChart" width="1200px" height="700px"></canvas>""" + f"""
        <script>
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {params});
        </script>
        """

    return prefix_chartjs

    

if __name__=="__main__":
    app.run(debug=True)