import re
import json
import random
import string
import compare
from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery

import sys

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

@views.route('/all_revisions', methods=('GET','POST'))
def show_all_revisions():
    all_revisions = DBQuery().get_all_revisions()
    data_list = []

    for revision in all_revisions:
        revision_id = revision.id
        feedback_id = revision.feedback_id
        feedback_order = revision.feedback_order
        created_user = revision.created_user

        article_id = revision.article_id
        article = DBQuery().get_article_by_id(article_id)
        feedback = DBQuery().get_feedback_by_id(feedback_id)
        article_authors = article.authors
        title = article.title

        data = {
            "revision_id": revision_id,
            "feedback_id": feedback_id,
            "feedback_order": feedback_order,
            "created_user": created_user,

            "article_content": feedback.content,

            "article_id": article_id,
            "article_authors": article_authors,
            "title": title
        }
        data_list.append(data)

    return render_template('show_all_revisions.html', data=data_list)

@views.route('/revision/<revision_id>', methods=('GET','POST'))
def show_revision(revision_id):

    revision = DBQuery().get_revision_by_id(int(revision_id))
    article = DBQuery().get_article_by_id(revision.article_id)

    data = {
        "revision_id": revision.id,
        "article_id": revision.article_id,
        "feedback_id": revision.feedback_id,
        "feedback_order": revision.feedback_order,
        "revision_content": revision.revision_content,
        "created_user": revision.created_user,

        "article_title": article.title,
        "article_content": article.content,
        "article_authors": article.authors
    }
    return render_template('revision.html',data=data)

###############################################
#      Revision Task - ensemble feedback      #
###############################################
@views.route('/ensemble/<feedback_id>', methods=('GET','POST'))
def ensemble_feedback(feedback_id):
    verified_string = generate_verified_str(6)
    experiment_flow = request.args.get('flow', default="")
    create_user = request.args.get('user', default="")
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
        "create_user": create_user,
        "article_content": article_content,
        "feedback_content": json.dumps(feedback_content),

        "verified_string": verified_string,
        "experiment_flow": experiment_flow,
    }

    return render_template('ensemble_feedback.html', data=data)


# For experiment
@views.route('/pre_experiment', methods=('GET','POST'))
def pre_experiment():
    # experiment flow pattern:
    # <feedback_id1>-<order1>|<feedback_id2>-<order2>|<feedback_id3>-<order3>
    experiment_flow = request.args.get('flow', default="")
    create_user = request.args.get('user', default=None)
    feedback_ids = []
    orders = []
    done = []

    flow = experiment_flow.split("|")
    for element in flow:
        [feedback_id, order] = element.split("-")
        feedback_ids.append(feedback_id)
        orders.append(order)
        revision = DBQuery().get_revision_by_feedback_id_and_user(feedback_id, create_user)
        if revision is None:
            done.append(0)
        else:
            done.append(1)

    data = {
        "experiment_flow": experiment_flow,
        "create_user": create_user,

        "feedback_id1": feedback_ids[0],
        "order1": orders[0],
        "order1_done": done[0],

        "feedback_id2": feedback_ids[1],
        "order2": orders[1],
        "order2_done": done[1],

        "feedback_id3": feedback_ids[2],
        "order3": orders[2],
        "order3_done": done[2],
    }

    return render_template('pre_experiment.html', data=data)


# For experiment
@views.route('/experiment/<feedback_id>', methods=('GET','POST'))
def experiment(feedback_id):
    create_user = request.args.get('user', default="")
    order = request.args.get('order', default="")
    experiment_flow = request.args.get('flow', default="")
    feedback = DBQuery().get_feedback_by_id(feedback_id)
    article = DBQuery().get_article_by_id(feedback.article_id)
    article_title = article.title


    data = {
        "article_title": article_title,
        "feedback_id": feedback_id,
        "order": order,
        "experiment_flow": experiment_flow,
        "create_user": create_user,
    }

    return render_template('experiment.html', data=data)


# For experiment
@views.route('/experiment_article/<feedback_id>', methods=('GET','POST'))
def experiment_article(feedback_id):
    verified_string = generate_verified_str(6)

    create_user = request.args.get('user', default="")
    order = request.args.get('order', default="")
    experiment_flow = request.args.get('flow', default="")

    sys.stderr.write("id: " + str(feedback_id))
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

        "verified_string": verified_string,
        "experiment_flow": experiment_flow,
    }

    return render_template('experiment_article.html', data=data)


@views.route('/success')
def success():
    verified_string = request.args.get('verified_string')
    experiment_flow = request.args.get('flow', default="")
    create_user = request.args.get('user', default="")
    if not verified_string:
        data = {}
    else:
        data = {
            "verified_string": verified_string,
            "experiment_flow": experiment_flow,
            "create_user": create_user,
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
