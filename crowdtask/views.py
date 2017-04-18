import re
import json
import random
import string

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

    all_articles = DBQuery().get_all_articles()    
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
def comparison_task():
    #generate verified_code
    verified_string = generate_verified_str(6)


    data = {
        "verified_string": verified_string
    }
    return render_template('comparison_task.html', data=data)

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
