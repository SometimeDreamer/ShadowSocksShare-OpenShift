#!/usr/bin/env python
# -*- utf-8 -*-
import base64
import random
import logging
import time
import threading
import os
from app import app
from app.ascii import birthday_2017, ss_title
from app.ss import ss_free
from app import donation
from flask import render_template, send_from_directory, abort


servers = list()
curtime = time.ctime()

# decoded = list()
# for i in servers:
#     for j in i['data']:
#         decoded.append(j['ssr_uri'])
# decoded = '\n'.join(decoded)
# encoded = base64.urlsafe_b64encode(bytes(decoded, 'utf-8'))
encoded = ''
full_encoded = ''
jsons = list()
full_jsons = list()


def update_servers():
    try:
        # servers
        global servers
        servers = ss_free.main()
        # subscription
        global encoded
        global full_encoded
        global jsons
        global full_jsons
        jsons = list()
        decoded = list()
        full_decoded = list()
        for website in servers:
            for server in website['data']:
                full_decoded.append(server['ssr_uri'])
                full_jsons.append(server['json'])
                if server['status'] is True:
                    decoded.append(server['ssr_uri'])
                    jsons.append(server['json'])

        decoded = '\n'.join(decoded)
        encoded = base64.urlsafe_b64encode(bytes(decoded, 'utf-8'))
        full_decoded = '\n'.join(full_decoded)
        full_encoded = base64.urlsafe_b64encode(bytes(full_decoded, 'utf-8'))
    except Exception as e:
        logging.exception(e, stack_info=True)


# counter_path = os.path.expanduser('/tmp/counter')
counter_path = 'memory'
count = 0


def counter(counter_path=counter_path):
    if counter_path == 'memory':
        global count
        count += 1
    else:
        if not os.path.exists(os.path.split(counter_path)[0]):
            os.makedirs(os.path.split(counter_path)[0])
        if not os.path.exists(counter_path):
            open(counter_path, 'w').write('0')
        count = int(open(counter_path).readline())
        open(counter_path, 'w').write(str(count + 1))
    if count % 150 == 2:
        update_thread = threading.Thread(target=update_servers)
        update_thread.start()
    return count


def gen_canvas_nest():
    """为背景很绚丽的特效生成随机参数
    """
    color = ','.join([str(random.randint(0, 255)) for i in range(3)])
    opacity = str(random.random() + 0.5)
    count = str(random.randint(0, 150))
    return color, opacity, count


@app.route('/')
def index():
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            'index.html',
            servers=servers,
            ss=ss_title[random.randint(0, len(ss_title) - 1)],
            counter=counter(),
            color=color,
            opacity=opacity,
            count=count,
            ctime=curtime,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/full')
def full():
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            'full.html',
            servers=servers,
            ss=ss_title[random.randint(0, len(ss_title) - 1)],
            counter=counter(),
            color=color,
            opacity=opacity,
            count=count,
            ctime=curtime,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/<string:path>')
def pages(path):
    print(path)
    try:
        a, b = path.split('-')
        a, b = int(a), int(b)
    except Exception:
        abort(404)

    if a >= len(servers):
        abort(404)
    elif b >= len(servers[a]['data']):
        abort(404)

    try:
        uri = servers[a]['data'][b]['decoded_url'] if 'decoded_url' in servers[a]['data'][b] else ''
        remarks = servers[a]['data'][b]['remarks'] if 'remarks' in servers[a]['data'][b] else 'None'
        server = servers[a]['data'][b]['server'] if 'server' in servers[a]['data'][b] else 'None'
        server_port = servers[a]['data'][b]['server_port'] if 'server_port' in servers[a]['data'][b] else 'None'
        password = servers[a]['data'][b]['password'] if 'password' in servers[a]['data'][b] else 'None'
        method = servers[a]['data'][b]['method'] if 'method' in servers[a]['data'][b] else 'None'
        ssr_protocol = servers[a]['data'][b]['ssr_protocol'] if 'ssr_protocol' in servers[a]['data'][b] else 'None'
        obfs = servers[a]['data'][b]['obfs'] if 'obfs' in servers[a]['data'][b] else 'None'
        href = servers[a]['data'][b]['href'] if 'href' in servers[a]['data'][b] else 'None'
        json = servers[a]['data'][b]['json'] if 'json' in servers[a]['data'][b] else 'None'
        obfsparam = servers[a]['data'][b]['obfsparam'] if 'obfsparam' in servers[a]['data'][b] else 'None'
        protoparam = servers[a]['data'][b]['protoparam'] if 'protoparam' in servers[a]['data'][b] else 'None'
        status = servers[a]['data'][b]['status'] if 'status' in servers[a]['data'][b] else 'None'

        color, opacity, count = gen_canvas_nest()

        return render_template(
            'pages.html',
            uri=uri,
            server=server,
            server_port=server_port,
            password=password,
            method=method,
            ssr_protocol=ssr_protocol,
            obfs=obfs,
            href=href,
            remarks=remarks,
            counter=counter(),
            server_data=servers[a]['data'][b],
            color=color,
            opacity=opacity,
            count=count,
            json=json,
            obfsparam=obfsparam,
            protoparam=protoparam,
            status=status,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/html/<path:path>')
def static_html(path):
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            path,
            color=color,
            opacity=opacity,
            count=count,)
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/donation')
def html_donation():
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            'donate.html',
            color=color,
            opacity=opacity,
            count=count,
            data=donation.data,
            sum_people=donation.sum_people,
            sum_money=donation.sum_money)
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/subscribe')
def subscribe():
    return encoded


@app.route('/full/subscribe')
def full_subscribe():
    return full_encoded


@app.route('/json')
def subscribe_json():
    return '{}' if len(jsons) == 0 else random.sample(jsons, 1)[0]


@app.route('/full/json')
def full_subscribe_json():
    return '{}' if len(jsons) == 0 else random.sample(full_jsons, 1)[0]


@app.route('/js/<path:path>')
def send_jsadfsadfs(path):
    return send_from_directory('js', path)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    color, opacity, count = gen_canvas_nest()
    return render_template(
        '404.html',
        color=color,
        opacity=opacity,
        count=count,
    ), 404


@app.route('/gift')
def gift():
    return birthday_2017


print('部署完成')
