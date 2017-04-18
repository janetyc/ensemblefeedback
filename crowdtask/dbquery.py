from crowdtask.models import Article, Feedback, Revision
from crowdtask.models import Task
from crowdtask import db
from enum import TaskType

class DBQuery(object):
    # ************************************************** #
    #               Add data from database               #
    # ************************************************** #
    # article
    def add_article(self, title, content, authors, source, year):
        article = Article(title, content, authors, source, year)
        db.session.add(article)
        db.session.commit()

        return article.id

    def add_feedback(self, article_id, content, feedback_content):
        feedback = Feedback(article_id, content, feedback_content)
        db.session.add(feedback)
        db.session.commit()

        return feedback.id

    def add_revision(self, created_user, article_id, feedback_id, feedback_order, feedback_content, revision_content, duration_time):
        revision = Revision(created_user, article_id, feedback_id, feedback_order, feedback_content, revision_content, duration_time)
        db.session.add(revision)
        db.session.commit()

        return revision.id

    # crowd task
    def add_task(self, created_user, task_type, problem, answer,
                 verified_string):

        task = Task(created_user, task_type, problem, answer, verified_string)
        db.session.add(task)
        db.session.commit()
        return task.id
    

    # ************************************************** #
    #               Get data from database               #
    # ************************************************** #

    def get_task_by_code(self, code):
        task = Task.query.filter_by(verified_string=code).first()
        return task

    def get_all_tasks(self):
        all_tasks = Task.query.all()
        return all_tasks

    # article
    def get_article_by_id(self, article_id):
        article = Article.query.filter_by(id=article_id).first()
        return article

    def get_article_by_title(self, title):
        article = Article.query.filter_by(title=title).first()
        return article

    def get_article_by_title_and_authors(self, title, authors):
        article = Article.query.filter_by(title=title, authors=authors).first()
        return article

    def get_all_articles(self):
        all_articles = Article.query.all()
        return all_articles

    def get_article_count(self):
        return Article.query.count()

    def get_article_paginate(self, page, per_page):
        articles = Article.query.order_by(Article.created_time.desc()).paginate(page=page, per_page=per_page)
        return articles

    # feedback
    def get_feedback_by_id(self, feedback_id):
        feedback = Feedback.query.filter_by(id=feedback_id).first()
        return feedback

    # revision
    def get_revision_by_id(self, revision_id):
        revision = Revision.query.filter_by(id=revision_id).first()
        return revision


    # ************************************************** #
    #               Update data from database            #
    # ************************************************** #


