import os
import time
from flask import Flask, Response, jsonify, request

from bibtex_resolver.crossref import retreive_bibtex

app = Flask(__name__)

@app.route('/')
def index():
    print('Hello World!')
    f =  app.send_static_file('html/index.html')
    return f

@app.route('/js/<path:path>')
def static_proxy(path):
    return app.send_static_file(os.path.join('js', path))

@app.route('/api')
def api():
    start = time.time()
    results = retreive_bibtex(request.args['q'])
    end = time.time()

    print(end-start)
    return results


if __name__ == '__main__':
    app.debug = True
    app.run()

