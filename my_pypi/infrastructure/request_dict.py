import flask
from flask import Request
from werkzeug.datastructures import MultiDict

class RequestDictionary(dict):
    def __init__(self, *args, default_val=None, **kwargs):
        self.default_val = default_val
        super().__init__(*args, **kwargs)

    #make the dict.value trick
    def __getattr__(self, key):
        return self.get(key, self.default_val)

def create(default_val=None, **route_args) -> RequestDictionary:
    ''' This function provide a clean approach to data the incomes from
        the web, no-matter by which way the user pass a data(URL query, header, body, routes arguments..)
        it will fetch the data by priorities'''
    request = flask.request
    args = request.args
    if isinstance(request.args, MultiDict):
        args = request.args.to_dict()

    form = request.form
    if isinstance(request.args, MultiDict):
        form = request.form.to_dict()

    data = {
        **args,
        **request.headers,
        **form,
        **route_args  # should be passed by route
    }
    return RequestDictionary(data, default_val=default_val)
