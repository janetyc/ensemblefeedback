import json

from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery
from enum import TaskType
from datetime import datetime


api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/add_comparison', methods=('GET','POST'))
def add_topic():
    article_id = request.args.get('article_id')
    worker_id = request.args.get('worker_id', u'tester')
    verified_string = request.args.get('verified_string')


@api.route('/api/add_article', methods=('GET','POST'))
def add_article():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        
        list = content.strip().split("\n")
        list = [i.strip() for i in list if i]
        
        article_title = title.strip()
        article_content = "<BR>".join(list)
        article_authors = author.strip()
        article_source = "structfeed"
        article_year = datetime.utcnow().year
        article_id = DBQuery().add_article(article_title, article_content, article_authors, article_source, article_year)

        data = {
            "author": author,
            "title": title,
            "content": content,
            "article_id": article_id
        }
        return jsonify(success=1, data=data)
    else:
        return jsonify(success=0, data=[])

@api.route('/api/add_revision', methods=('GET','POST'))
def add_revision():
    if request.method == 'POST':
        created_user = request.form['created_user']
        article_id = int(request.form['article_id'])
        feedback_id = int(request.form['feedback_id'])
        feedback_content = json.loads(request.form['feedback_content'])
        revision_content = json.loads(request.form['revision_content'])
        duration_time = int(request.form['duration_time'])
        
        revision_id = DBQuery().add_revision(created_user, article_id, feedback_id, feedback_content, revision_content, duration_time)

        data = {
            "created_user": created_user,
            "article_id": article_id,
            "feedback_id": feedback_id,
            "feedback_content": feedback_content,
            "duration_time": duration_time
        }

        return jsonify(success=1, data=data)
    else:
        return jsonify(success=0, data=[])        
    