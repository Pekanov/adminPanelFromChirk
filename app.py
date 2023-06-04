import requests as requests
import json
from flask import Flask, render_template, request, jsonify, redirect, make_response
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

host = os.getenv('HOST')
port = os.getenv('PORT')

# formatted_host = f'{host}:{port}'

filename = "tokens.json"
HOST = f'{host}:{port}'
# HOST = 'localhost:8080'



# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# @app.route('/admin_authorization', methods=['GET', 'POST'])
# def authorization():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         # Отправляем POST-запрос на сервер Spring
#         url ='http://'+HOST+'/user/authorisation'
#         data = {
#             'email': email,
#             'password': password
#         }
#         response = requests.post(url, json=data)
#
#         if response.status_code == 200:
#             # Сохраняем ответ от сервера Spring в JSON
#             json_response = response.json()
#
#             save_json_response(json_response)
#
#             return redirect('/admin_panel')  # Возвращаем JSON-ответ
#
#     return render_template("authorization.html")
#
#
# @app.route('/admin_panel', methods=['GET', 'POST'])
# def admin_panel():
#     if request.method == 'GET':
#         url = 'http://' + HOST + '/adminPanel'
#         headers = {'Authorization': 'Bearer ' + get_access_token_from_file()}
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             users = response.json()  # Получаем список пользователей
#             return render_template("adminPanel.html", users=users)
#
#     if request.method == 'POST':
#         if 'filter_value' in request.form:
#             user_filter = request.form['userFilter']
#             if user_filter == '':
#                 return redirect('/admin_panel')
#
#             filter_value = request.form.get('filter_value')
#             url = 'http://' + HOST + '/adminPanel/byFilter'
#
#             if filter_value == 'true':
#                 value = True
#             else:
#                 value = False
#
#             data = {'search': user_filter, 'filterByEmail': value}
#
#             # response = requests.post(url, json=data)
#             # response = requests.get(url, user_filter, filter_value)
#             response = requests.get(url, json=data)
#
#             if response.status_code == 200:
#                 users = response.json()  # Получаем список пользователей
#                 return render_template("adminPanel.html", users=users)
#             else:
#                 return 'Error: ' + str(response.status_code)
#
#         if 'value' in request.form:
#             moderator_checked = request.form.get('value')
#             email = request.form['email']
#             data = {'email': email}
#
#             if moderator_checked == 'true':
#                 url = 'http://' + HOST + '/adminPanel/addAdmin'
#             else:
#                 url = 'http://' + HOST + '/adminPanel/deleteAdmin'
#
#             response = requests.post(url,email)
#
#             if response.status_code == 200:
#                 return redirect('/admin_panel')
#             else:
#                 return 'Error: ' + str(response.status_code)
#
#
#
#
#     return 'Invalid request'
#
#
# def save_json_response(json_response):
#     with open(filename, 'w') as file:
#         file.seek(0)  # Перемещаемся в начало файла
#         file.truncate()  # Очищаем содержимое файла
#         json.dump(json_response, file)
#
#
# def get_access_token_from_file():
#     with open(filename) as file:
#         json_data = json.load(file)
#         return json_data['accessToken']
#
#
# def get_refresh_token_from_file():
#     with open(filename) as file:
#         json_data = json.load(file)
#         return json_data['refreshToken']
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)



def save_tokens_to_cookie(access_token, refresh_token):
    response = make_response(redirect('/admin_panel'))
    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)
    return response


def get_access_token_from_cookie():
    return request.cookies.get('access_token')


def get_refresh_token_from_cookie():
    return request.cookies.get('refresh_token')


def clear_tokens_from_cookie():
    response = make_response(redirect('/admin_authorization'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


def check_authentication():
    if (
        request.endpoint == 'admin_panel'
        and not request.path.startswith('/admin_authorization')
        and not get_access_token_from_cookie()
    ):
        return redirect('/admin_authorization')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/admin_authorization', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        url = 'http://' + HOST + '/user/authorisation'
        data = {
            'email': email,
            'password': password
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response['accessToken']
            refresh_token = json_response['refreshToken']
            return save_tokens_to_cookie(access_token, refresh_token)

    return render_template("authorization.html")


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'GET':
        url = 'http://' + HOST + '/adminPanel'
        headers = {'Authorization': 'Bearer ' + get_access_token_from_cookie()}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            users = response.json()
            return render_template("adminPanel.html", users=users)

    if request.method == 'POST':
        if 'filter_value' in request.form:
            user_filter = request.form['userFilter']
            if user_filter == '':
                return redirect('/admin_panel')

            filter_value = request.form.get('filter_value')
            url = 'http://' + HOST + '/adminPanel/byFilter'

            if filter_value == 'true':
                value = True
            else:
                value = False

            data = {'search': user_filter, 'filterByEmail': value}

            # response = requests.post(url, json=data)
            # response = requests.get(url, user_filter, filter_value)
            response = requests.get(url, json=data)

            if response.status_code == 200:
                users = response.json()  # Получаем список пользователей
                return render_template("adminPanel.html", users=users)
            else:
                return 'Error: ' + str(response.status_code)

        if 'value' in request.form:
            headers = {'Authorization': 'Bearer ' + get_access_token_from_cookie()}
            moderator_checked = request.form.get('value')
            email = request.form['email']
            data = {'email': email}

            if moderator_checked == 'true':
                url = 'http://' + HOST + '/adminPanel/addAdmin'
            else:
                url = 'http://' + HOST + '/adminPanel/deleteAdmin'

            response = requests.post(url,email, headers=headers)

            if response.status_code == 200:
                return redirect('/admin_panel')
            else:
                return 'Error: ' + str(response.status_code)

    return 'Invalid request'


@app.route('/logout')
def logout():
    return clear_tokens_from_cookie()


if __name__ == '__main__':
    app.before_request(check_authentication)
    app.run(debug=True)
