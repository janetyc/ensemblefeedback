import re
import json
import random
import string
import compare
from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery

per_page = 10
views = Blueprint('views', __name__, template_folder='templates')


@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@views.route('/all_articles', methods=['GET', 'POST'])
@views.route('/all_articles/<int:page>', methods=['GET', 'POST'])
def show_all_articles(page=1):
    paginated_articles = DBQuery().get_article_paginate(page, per_page)
    return render_template('show_all_articles.html', paginated_articles=paginated_articles)

@views.route('/all')
def show_all():

    all_articles = DBQuery().get_article_count()    
    article_authors = "anonymous"
    data_list = []
    
    for article in all_articles:
        article_id = article.id
        title = article.title.encode("utf-8")

        if article.authors:
            article_authors = article.authors
        
        data = {
            "title": title,
            "article_id": article_id,
            "authors": article_authors
        }
        data_list.append(data)

    data_list.sort(key=lambda tup: tup["article_id"])

    return render_template('show_all.html', data=data_list)

@views.route('/ensemble_all', methods=('GET','POST'))
def show_ensemble_all():
    all_ensemble_feedback = DBQuery().get_all_feedbacks()
    data_list = []

    for feedback in all_ensemble_feedback:
        feedback_id = feedback.id
        article_id = feedback.article_id
        article = DBQuery().get_article_by_id(article_id)
        article_authors = article.authors
        title = article.title

        data = {
            "feedback_id": feedback_id,
            "title": title,
            "article_id": article_id,
            "authors": article_authors
        }
        data_list.append(data)

    return render_template('show_all_feedbacks.html', data=data_list)


@views.route('/comparison', methods=('GET','POST'))
def get_compair_pair():
    verified_string = generate_verified_str(6)

    method = request.args.get('mode', default="diff")
    times = request.args.get('ref', default="0")
    pair_id = request.args.get('pair', default="")
    if pair_id == "":
        uncompare = DBQuery().get_uncompare_list()
        if not uncompare:
            if int(times) > 0:
                return show_verify(verified_string)
            else:
                return render_template('task_finish.html')
        else:
            pair_id = DBQuery().get_compare_by_id(random.choice(uncompare)).pair_id
    return comparison_task(pair_id, method, verified_string, times)


def comparison_task(pair_id, method, code, times):
    [p1, p2] = pair_id.split("_")

    article1 = DBQuery().get_article_by_id(p1)
    paragraphs1 = article1.content.split("<BR>")
    article2 = DBQuery().get_article_by_id(p2)
    paragraphs2 = article2.content.split("<BR>")

    list1 = []
    for i, paragraph in enumerate(paragraphs1):
        list1.append((i, paragraph))
    list2 = []
    for i, paragraph in enumerate(paragraphs2):
        list2.append((i, paragraph))

    sorted(list1)
    sorted(list2)
    data = {
        "text1": {
            "id": article1.id,
            "title": article1.title,
            "authors": article1.authors,
            "paragraphs": list1
            },
        "text2": {
            "id": article2.id,
            "title": article2.title,
            "authors": article2.authors,
            "paragraphs": list2
            },
        }
    if method == "diff":
        [diff1, diff2] = compare.compareText(article1.content, article2.content)
        return render_template('comparison_task.html', method=method,
                               pair_id=pair_id, data=data, code=code,
                               diff1=diff1, diff2=diff2, times=times)

    return render_template('comparison_task.html', method=method,
                           pair_id=pair_id, data=data, code=code, times=times)


@views.route('/verified/<verified_string>', methods=('GET','POST'))
def show_verify(verified_string):
    return render_template('verified_code.html', code=verified_string)


@views.route('/article/<article_id>', methods=('GET','POST'))
def show_article(article_id):
    article = DBQuery().get_article_by_id(article_id)
    paragraphs = article.content.split("<BR>")
    
    list = []
    for i, paragraph in enumerate(paragraphs):
        list.append((i, paragraph))

    sorted(list)
    data = {
       "id": article.id, 
       "title": article.title,
       "authors": article.authors,
       "paragraphs": list,

    }

    return render_template('article.html', data=data)


###############################################
#      Revision Task - ensemble feedback      #
###############################################
@views.route('/ensemble/<feedback_id>', methods=('GET','POST'))
def ensemble_feedback(feedback_id):
    verified_string = generate_verified_str(6)
    feedback = DBQuery().get_feedback_by_id(feedback_id)
    article_id = None
    article_content = ""
    feedback_content = ""
    if feedback:        
        article_id = feedback.article_id
        content = feedback.content.strip()
        feedback_content = feedback.feedback_content
        content_list = content.split("\n")
        article_content = "\n".join(content_list)

    data = {
        "article_id": article_id,
        "feedback_id": feedback_id,
        "article_content": article_content,
        "feedback_content": json.dumps(feedback_content),

        "verified_string": verified_string
    }

    return render_template('ensemble_feedback.html', data=data)


# For experiment
@views.route('/experiment/<feedback_id>', methods=('GET','POST'))
def experiment(feedback_id):
    create_user = request.args.get('user', default="")
    order = request.args.get('order', default="")

    data = {
        "feedback_id": feedback_id,
        "order": order,
        "create_user": create_user,
    }

    return render_template('experiment.html', data=data)


# For experiment
@views.route('/experiment_article/<feedback_id>', methods=('GET','POST'))
def experiment_article(feedback_id):
    verified_string = generate_verified_str(6)

    create_user = request.args.get('user', default="")
    order = request.args.get('order', default="")

    feedback = DBQuery().get_feedback_by_id(feedback_id)
    article_id = feedback.article_id
    article = DBQuery().get_article_by_id(article_id)
    paragraphs = article.content.split("<BR>")

    list = []
    for i, paragraph in enumerate(paragraphs):
        list.append((i, paragraph))

    sorted(list)

    data = {
        "article_id": article_id,
        "title": article.title,
        "authors": article.authors,
        "paragraphs": list,

        "feedback_id": feedback_id,
        "order": order,
        "create_user": create_user,

        "verified_string": verified_string
    }

    return render_template('experiment_article.html', data=data)


@views.route('/success')
def success():
    verified_string = request.args.get('verified_string')
    if not verified_string:
        data = {}
    else:
        data = {
            "verified_string": verified_string
        }
    return render_template('success.html', data=data)


def generate_verified_str(number):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(number))

# error page
@views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@views.app_errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400
