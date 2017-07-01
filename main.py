from flask import Flask, render_template, request, json
import requests, bs4, os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/get_title", methods=['GET'])
def get():
    if request.args.get('url') is None:
        return render_template('index.html')
    else:
        url = request.args.get('url')
        z = dict()
        z['url'] = url

        r = requests.get(url)
        if r.status_code != 200:
            z['return_code'] = r.status_code
        else:
            z['return_code'] = r.status_code

            page = bs4.BeautifulSoup(r.text, "html.parser")
            z['title'] = page.title.text

        return json.jsonify(z)

port = int(os.environ.get('PORT', 33507))
app.run(host='0.0.0.0', port=port)
