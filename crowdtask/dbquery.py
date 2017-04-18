from crowdtask.models import Article
from crowdtask.models import Task
from crowdtask.models import Comparison
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

    def add_comparison(self, pair_id, created_user,
                       article1_chosen, article2_chosen, better_one):
        comparison = Comparison(pair_id, created_user,
                                article1_chosen, article2_chosen, better_one)
        db.session.add(comparison)
        db.session.commit()
        return comparison.id

    # ************************************************** #
    #               Update data from database            #
    # ************************************************** #

    def update_better(self, pair_id):
        [article1, article2] = pair_id.split("_")
        comparison = Comparison.query.filter_by(pair_id=pair_id).first()
        if comparison.article1_chosen >= 2:
            comparison.better_one = int(article1)
        elif comparison.article2_chosen >= 2:
            comparison.better_one = int(article2)
        db.session.commit()
        return comparison.id

    def update_comparison(self, pair_id, created_user, choosed_article):
        comparison = Comparison.query.filter_by(pair_id=pair_id).first()
        if int(choosed_article) == 1:
            comparison.article1_chosen = comparison.article1_chosen + 1
        elif int(choosed_article) == 2:
            comparison.article2_chosen = comparison.article2_chosen + 1
        self.update_better(pair_id)
        db.session.commit()
        return comparison.id

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

    def get_compare_count(self):
        return Comparison.query.count()

    def get_compare_by_id(self, compare_id):
        comparison = Comparison.query.filter_by(id=compare_id).first()
        return comparison

    def get_compare_better(self, pair_id):
        comparison = Comparison.query.filter_by(pair_id=pair_id).first()
        return comparison.better_one

    def get_uncompare_list(self):
        uncompare = []
        count = self.get_compare_count()
        for compare_id in range(1, count + 1):
            if self.get_compare_by_id(compare_id).better_one == 0:
                uncompare.append(compare_id)
        return uncompare
