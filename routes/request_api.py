
from flask_cors import cross_origin
from flask import request, Blueprint, make_response, render_template
from guesslang import Guess

from tools import *

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/language', methods=['GET'])
@cross_origin(supports_credentials=True)
def language():
    code = request.values.get('code', '')
    if not code:
        response = make_response(render_template('api.txt'))
        response.headers["Content-Type"] = "text/plain"
        return response
    guess = Guess()
    language = guess.language_name(code)

    response = make_response(language)
    response.headers["Content-Type"] = "text/plain"
    return response


@REQUEST_API.route('/highlight', methods=['GET'])
@cross_origin(supports_credentials=True)
def highlight():
    code = request.values.get('code', '')
    if not code:
        response = make_response(render_template('api.txt'))
        response.headers["Content-Type"] = "text/plain"
        return response

    lexer = request.values.get('lexer', '')
    options = request.values.get('options', '')

    def convert(item):
        key, value = item
        if value == 'False':
            return key, False
        elif value == 'True':
            return key, True
        else:
            return key, value
    options = dict(convert(option.split('='))
                   for option in options.split(',') if option)

    style = request.values.get('style', '')
    linenos = request.values.get('linenos', '')
    divstyles = request.form.get('divstyles', get_default_style())

    html = hilite_me(code, lexer, options, style, linenos, divstyles)
    response = make_response(html)
    response.headers["Content-Type"] = "text/plain"
    return response
