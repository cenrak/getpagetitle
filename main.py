from flask import Flask, render_template, request, json
from flask_cors import CORS, cross_origin

import requests, bs4, os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
"""
route('/') renders index.html, which shows nothing but how to use this app
"""
@app.route("/", methods=['GET'])
def hello():
    return render_template('index.html')

"""
route('get_title') cares about 1 GET argument, GET['url']. As of now, there is
no encoding whatsoever performed on the argument.

If the page does not see GET['url'], it redirects to index.html.

If the there is GET['url'], the app will try to get the page, if it fails, it will
send a json with an error message to check the URL or with the status code.
"""
@app.route("/get_title", methods=['GET'])
@cross_origin()
def get():
    if request.args.get('url') is None:
        return render_template('index.html')
    else:
        url = request.args.get('url')
        z = dict()
        z['url'] = url

        try:
            r = requests.get(url)
        except:
            z['message'] = 'Check URL'
            return json.jsonify(z)

        if r.status_code != 200:
            z['return_code'] = r.status_code
        else:
            z['return_code'] = r.status_code

            page = bs4.BeautifulSoup(r.text, "html.parser")
            z['title'] = page.title.text

        return json.jsonify(z)

port = int(os.environ.get('PORT', 33507))
app.run(host='0.0.0.0', port=port)
