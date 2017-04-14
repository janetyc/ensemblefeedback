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
