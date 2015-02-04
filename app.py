import os
import sys
import time
import logging
from logging import StreamHandler
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
    app.logger.info(results)
    app.logger.info('Request Time: %.4f', end-start)
    return results


# log to stderr
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)


if __name__ == '__main__':
    app.debug = True
    app.run()

