from crowdtask.models import Article
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

    # crowd task
    def add_task(self, created_user, task_type, problem, answer,
                 verified_string):

        task = Task(created_user, task_type, problem, answer, verified_string)
        db.session.add(task)
        db.session.commit()
        return task.id


    # ************************************************** #
    #               Update data from database            #
    # ************************************************** #
    

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

