from datetime import datetime
from crowdtask import db


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())
    created_time = db.Column(db.DateTime())
    authors = db.Column(db.Text())
    source = db.Column(db.Text())
    year = db.Column(db.Integer)

    def __init__(self, title, content, authors, source, year):
        self.title = title
        self.content = content
        self.created_time = datetime.utcnow()
        self.authors = authors
        self.source = source
        self.year = year

    def __repr__(self):
        return '<Article %r>' % self.title


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_user = db.Column(db.Text())
    task_type = db.Column(db.Text())
    problem = db.Column(db.Text())  # article_id|paragraph_idx
    answer = db.Column(db.Text())  # list of output_ids (e.g. relation_id, topic_id, relevance_id)
    verified_string = db.Column(db.Text())
    created_time = db.Column(db.DateTime())
    submited_time = db.Column(db.DateTime())

    hitId = db.Column(db.Text())
    assignmentId = db.Column(db.Text())

    def __init__(self, created_user, task_type, problem, answer, verified_string):
        self.created_user = created_user
        self.task_type = task_type
        self.problem = problem
        self.answer = answer
        self.verified_string = verified_string
        self.created_time = datetime.utcnow()
        self.submited_time = datetime.utcnow()

    def __repr__(self):
        return '<Task %r>' % self.created_user


class Comparison(db.Model):
    __tablename__ = 'comparison'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pair_id = db.Column(db.Text())
    created_user = db.Column(db.Text())
    article1_chosen = db.Column(db.Integer())
    article2_chosen = db.Column(db.Integer())
    better_one = db.Column(db.Integer())

    created_time = db.Column(db.DateTime())

    def __init__(self, pair_id, created_user,
                 article1_chosen, article2_chosen, better_one):
        self.pair_id = pair_id
        self.created_user = created_user
        self.article1_chosen = article1_chosen
        self.article2_chosen = article2_chosen
        self.better_one = better_one
        self.created_time = datetime.utcnow()

    def __repr__(self):
        return '<Topic %r>' % self.created_user
