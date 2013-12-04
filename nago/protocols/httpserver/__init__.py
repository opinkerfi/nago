#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A http server written in flask. Allows two or more nago instances to talk with each other

"""
# this is a workaround for rhel6 systems where python-jinja has multiple versions
# installed at the same time
# https://bugzilla.redhat.com/show_bug.cgi?id=867105
__requires__ = ['jinja2 >= 2.4']
import pkg_resources


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from functools import wraps
import nago.core
import nago.extensions
import json



app = Flask(__name__)
app.secret_key = 'bla'


def login_required(func, permission=None):
    """ decorate with this function in order to require a valid token for any view

     If no token is present you will be sent to a login page
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not check_token():
            return login()
        elif not nago.core.has_access(session.get('token')):
            return http403()
        return func(*args, **kwargs)
    return decorated_function





def check_token():
    if 'token' in request.args :
        session['token'] = request.args.get('token')
    elif request.method == 'POST' and 'token' in request.form:
        session['token'] = request.form.get('token')

    if session.get('token'):
        return True
    else:
        return False


@app.route('/403', methods=['GET', 'POST'])
def http403():
    token = session.get('token')
    node = nago.core.get_node(token)
    if not node:
        # Check if remote machine sent us their info
        json_data = request.args.get('about_me', '{}')

        # Log down remote node ip address
        headers_list = request.headers.getlist("X-Forwarded-For")
        user_ip = headers_list[0] if headers_list else request.remote_addr

        node_info = json.loads(json_data)
        node = nago.core.register_node(token, node_info=node_info, address=user_ip)
    host_name = node.get('host_name') or ''
    return jsonify(token=token, message="Unauthorized access. This token is unsigned.", host_name=host_name)
    #return render_template('403.html', **locals()), 403

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    token = session.get('token')
    node = nago.core.get_node(token)

    my_info = nago.core.get_my_info()

    extension_dict = nago.extensions.get_extensions()
    extensions = {}
    for k, v in extension_dict.items():
        extensions[k] = {}
        extensions[k]['description'] = v.__doc__
        extensions[k]['shortdesc'] = str(v.__doc__).splitlines()[0]
        extensions[k]['methods'] = {}
        for name in nago.extensions.get_method_names(k):
            method = nago.extensions.get_method(k, name)
            extensions[k]['methods'][name] = {}
            extensions[k]['methods'][name]['description'] = method.__doc__
    return render_template('index.html', **locals())

@app.route('/nodes/', methods=['GET'])
@login_required
def list_nodes():
    """ Return a list of all nodes """
    token = session.get('token')
    node = nago.core.get_node(token)
    if not node.get('access') == 'master':
        return jsonify(status='error', error="You need master access to view this page")

    nodes = nago.core.get_nodes().values()
    return render_template('nodes.html', **locals())

@app.route('/nodes/<node_name>/', methods=['GET'])
@login_required
def node_detail(node_name):
    """ View one specific node """
    token = session.get('token')
    node = nago.core.get_node(token)
    if not node.get('access') == 'master':
        return jsonify(status='error', error="You need master access to view this page")

    node = nago.core.get_node(node_name)
    return render_template('node_detail.html', node=node)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')



@app.route('/esxtensions/<extension_name>/', methods=['GET', 'POST'])
@login_required
def extension(extension_name):
    token = session.get('token')
    node = nago.core.get_node(token) or {}
    host_name = node.get('host_name') or ''
    return render_template('index.html', **locals())


@app.route('/extensions/', methods=['GET'])
@login_required
def list_extensions():
    token = session.get('token')
    node = nago.core.get_node(token) or {}
    host_name = node.get('host_name') or ''
    extensions = nago.extensions.get_extensions()
    result = {}
    for k, v in extensions.items():
        result[k] = {}
        result[k]['description'] = v.__doc__
        result[k]['methods'] = {}
        for name in nago.extensions.get_method_names(k):
            method = nago.extensions.get_method(k, name)
            result[k]['methods'][name] = {}
            result[k]['methods'][name]['description'] = method.__doc__

    return jsonify(**result)



@app.route('/api/<extension_name>/<method_name>/', methods=['GET', 'POST'])
@login_required
def call_method(extension_name, method_name):
    kwargs = {}
    for k, v in request.args.items():
        kwargs[k] = v
    kwargs.pop('token', None)
    print kwargs.pop('about_me', None)
    kwargs.pop('json_data', None)
    token = session['token']
    result = {}
    result['result'] = nago.extensions.call_method(token=token, extension_name=extension_name, method_name=method_name, **kwargs)
    return jsonify(**result)


if __name__ == '__main__':
    app.run(debug=True)