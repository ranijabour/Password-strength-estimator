from flask import Flask, render_template, request, jsonify, session
import test
import pass_generator

app = Flask(__name__)
shared_data = ["", "", 0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/newpage')
def new_page():
    return render_template('generator.html')


@app.route('/password_meter', methods=['POST'])
def reverse_name():
    data = request.json
    password = data.get('password', '')
    username = data.get('username', '')
    country = data.get('country', '')
    rank, feedback1, feedback2, feedback3, feedback4, feedback5, indicators, info_list = test.main_index(username,
                                                                                                         password,
                                                                                                         country)
    response = {"rank": rank, "feedback1": feedback1, "feedback2": feedback2, "feedback3": feedback3,
                "feedback4": feedback4, "feedback5": feedback5, "indicators": indicators, "info_list": info_list}
    shared_data[0] = password
    shared_data[1] = username
    shared_data[2] = rank
    return jsonify(response)


@app.route('/new_password', methods=['POST'])
def new_password():
    data = request.json
    lucky_number = data.get('lucky_number', '')
    quote = data.get('quote', '')
    release = data.get('release', '')
    password = shared_data[0]
    username = shared_data[1]
    rank0 = shared_data[2]
    ranks, password, quote_release, with_quote, symbols_list, symbols_str, lucky_list, lucky_str = pass_generator.main(
        rank0, password, quote, release, lucky_number, username)
    response = {"ranks": ranks,
                "password": password,
                "quote_release": quote_release,
                "with_quote": with_quote,
                "symbols_list": symbols_list,
                "symbols_str": symbols_str,
                "lucky_list": lucky_list,
                "lucky_str": lucky_str}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
