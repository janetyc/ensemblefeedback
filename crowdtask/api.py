from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery
from enum import TaskType
from datetime import datetime

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/add_comparison', methods=('GET','POST'))
def add_comparison():
    if request.method == 'POST':
        pair_id = request.form['pair_id']  # articleId1_articleId2
        created_user = request.form['created_user']  # verified code
        choosed_article = request.form['choosed_article']  # 1 or 2

        comparison_id = DBQuery().update_comparison(pair_id, created_user, choosed_article)

        data = {
            "pair_id": pair_id,
            "created_user": created_user,
            "choosed_article": choosed_article,
            "comparison_id": comparison_id
        }
        return jsonify(success=1, data=data)
    else:
        return jsonify(success=0, data=[])


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

