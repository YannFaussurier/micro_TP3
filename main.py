#import pytrends
#import requests
from flask import Flask, render_template
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
from functools import wraps
import time
#def app(event):
#   return "Hey"


app = Flask(__name__)

# pytrends

pytrends = TrendReq(hl='en-US', tz=360)

#pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})



pytrends.build_payload(kw_list=['Kanye West','Michael Jackson'])



interest_over_time_df = pytrends.interest_over_time()

kanye = interest_over_time_df['Kanye West'].values.tolist()
mj = interest_over_time_df['Michael Jackson'].values.tolist()


dates = [datetime.fromtimestamp(int(date/1e9)).date().isoformat() for date in interest_over_time_df.index.values.tolist()]

params = { 
    "type": 'line',
    "data": {
    "labels": dates,
    "datasets": [{
        "data": kanye,
        "label": "kanye",
        "borderColor": "#3e95cd",
        "fill": 'false'
        },
        {
        "data": mj,
        "label": "Michael jackson",
        "borderColor": "#FF5733",
        "fill": 'false'
        }
        
        ]},
        
        "options": {
            "title": {
            "display": 'true',
            "text": 'comparison of kanye west and michael jackson over time'
            },
            "hover": {
            "mode": 'index',
            "intersect": 'true'
            },
        }
}


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper




@timeit
def hello_world():
 graph_script = """
 <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
        <canvas id="myChart" width="50" height="50"></canvas>""" + f"""
        <script>
        var ctx = document.getElementById('myChart');
        var myChart = new Chart(ctx, {params});
        </script>
 """
 return graph_script








@app.route('/', methods=["GET"])
def Show_graph():
    return hello_world()




if __name__=="__main__":
    app.run()