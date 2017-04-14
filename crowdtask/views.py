import re
import random
import string
from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery


views = Blueprint('views', __name__, template_folder='templates')


@views.route('/')
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


@views.route('/comparison', methods=('GET','POST'))
def comparison_task():
    data = []
    return render_template('comparison_task.html', data=data)

@views.route('/article/<article_id>', methods=('GET','POST'))
def show_article(article_id):

    if request.args.has_key('show_workflow'):
        show_workflow = request.args.get('show_workflow')
    else:
        show_workflow = 0

    article = DBQuery().get_article_by_id(article_id)
    paragraphs = article.content.split("<BR>")
    workflows = DBQuery().get_workflows_by_article_id(article_id)
    
    complete_workflow_list = []
    have_topic=False
    have_relevance=False
    for workflow in workflows:
        if workflow.topic_hit_ids and workflow.topic_hit_ids != "":
            have_topic = True

        if workflow.relevance_hit_ids and workflow.relevance_hit_ids != "":
            have_relevance = True
        
        if have_topic and have_relevance:
            complete_workflow_list.append(str(workflow.id))

    # crowd result
    if len(complete_workflow_list):
        crowd_result = (True, complete_workflow_list[0])
    else:
        crowd_result = (False, None)

    peer_count = DBQuery().get_peer_count_by_article_id(article_id)
    if peer_count:
        peer_result = (True, peer_count)
    else:
        peer_result = (False, peer_count)

    workflow_list = [str(workflow.id) for workflow in workflows]

    list = []
    for i, paragraph in enumerate(paragraphs):
        list.append((i, paragraph))

    sorted(list)
    data = {
       "id": article.id, 
       "title": article.title,
       "authors": article.authors,
       "paragraphs": list,
       "workflow_list": workflow_list,
       "show_workflow": show_workflow,
       "crowd_result": crowd_result,
       "peer_result": peer_result
    }

    return render_template('article.html', data=data)


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
