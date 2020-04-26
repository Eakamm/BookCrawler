#!coding=utf-8
from flask import Flask, jsonify, request
from manmanmai import ManManMai
import json
import MostWatchedBooks as mwb
import BookTop250WordCloud as btwc
import BookCommentsWordCloud as bcwc

app = Flask(__name__)


@app.route('/bookChart')
def hello_world():
    url = request.args.get('url')
    print(url)
    mmm = ManManMai()
    jd_url = mmm.get_jd_url(url)
    data = mmm.mmm(jd_url)
    print(json.dumps(data))
    return data


@app.route('/mostWatchedBook')
# def most_watched_book():
#     most_watched_book_list = mwb.run()
#     data = json.dumps(most_watched_book_list)
#     print(data)
#     return data
def most_watched_book():
    most_watched_book_list = btwc.run()
    data = json.dumps(most_watched_book_list)
    # print(data)
    return data


@app.route('/bookCommitsWordCloud')
def CommitsWordCloud():
    url = request.args.get('url')
    print(url)
    data = bcwc.run(url)
    print(data)
    return data


if __name__ == '__main__':
    app.run()
