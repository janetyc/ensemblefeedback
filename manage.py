import os
import re
import shutil
import json

from os import listdir
from os.path import isfile, join

from crowdtask import create_app, db
from crowdtask.models import *
from crowdtask.dbquery import DBQuery

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand


re_data = re.compile(r'(.*?): (.*?)\n')

app = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def dropdb():
    '''Drops all database tables.'''
    if prompt_bool('Are you sure to drop your databse?'):
        db.drop_all()


@manager.command
def init_comparison():
    # initialize comparison db
    start = 65
    end = 112
    for i in range(start, end + 1):
        for j in range(i + 1, end + 1):
            pair_id = str(i) + "_" + str(j)
            DBQuery().add_comparison(pair_id, "", 0, 0, 0)


@manager.command
def init_evaluate():
    # initialize evaluate db
    start = 111
    end = 112
    for i in range(start, end + 1):
        DBQuery().add_evaluate_by_revision_id(i)


@manager.option('-d', '--dir', dest='directory', default='data')
@manager.option('-n', '--filename', dest='filename', default=None)
def import_articles(directory, filename):
    '''Insert Articles to database.'''
    print "import articles from %s" % directory
    all_files = [file for file in listdir(directory) if isfile(join(directory, file))]

    for file in all_files:
        if file == ".DS_Store":
            continue
        print "Read Article: %s/%s ..." % (directory, file)
        r = open("%s/%s" % (directory, file), "r")
        content = r.read().decode('utf-8')
        all_match = re_data.findall(content)
        data = dict(all_match)

        article_title = data['Title'].strip()
        article_authors = data['Authors'].strip()
        article_source = data['Source'].strip()
        article_year = data['Year'].strip()
        article_content = data['Introduction'].strip()
        article_paragraphs = article_content.split('<BR>')

        #check whether article is exist
        article = DBQuery().get_article_by_title_and_authors(article_title, article_authors)
        if article:
            print "file exist!"
            if not isfile(join('data-in-db',file)):
                shutil.move('%s/%s' % (directory, file), 'data-in-db')
            continue

        print "insert article to the database ..."
        list = [i.strip() for i in article_paragraphs if i]
        clear_content = "<BR>".join(list)

        article_id = DBQuery().add_article(article_title, clear_content, article_authors, article_source, int(article_year))
        print "move article #%d to data-in-db folder ..." % article_id
        if isfile(join('data-in-db',file)):
            print "file has already existed in data-in-db folder..."
        else:
            shutil.move('%s/%s' % (directory, file), 'data-in-db')

@manager.option('-d', '--dir', dest='directory', default='feedback-data')
@manager.option('-n', '--filename', dest='filename', default=None)
def import_feedback(directory, filename):
    '''Insert Feedback to database.'''
    print "import feedback from %s" % directory

    all_files = [file for file in listdir(directory) if file.endswith('.json')]
    print all_files
    for file in all_files:
        fname = file[:-5] # remove ".json"
        txt_file = "%s.txt" % fname

        article_authors, article_title = fname.split("-")
        print [article_title.decode('utf-8'), article_authors.decode('utf-8')]
        article = DBQuery().get_article_by_title_and_authors(article_title, article_authors.decode('utf-8'))
        print article
        if not article:
            continue


        article_id = article.id
        print "Artcile id: %d" % article_id
        print "Read Feedback: %s/%s ..." % (directory, file)
        print "Read Article: %s/%s ..." % (directory, txt_file)
        fp_json = open("%s/%s" % (directory, file), "r")
        print fp_json
        fp_txt = open("%s/%s" % (directory, txt_file), "r")
        feedback_content = json.load(fp_json)
        content = fp_txt.read().decode('utf-8')
    
        print feedback_content
        print content
        print "insert feedback to the database ..."
        feedback_id = DBQuery().add_feedback(article_id, content, feedback_content)

        print "move feedback to feedback-in-db folder ..."
        if isfile(join('feedback-in-db',file)):
            print "file has already existed in feedback-in-db folder..."
        else:
            shutil.move('%s/%s' % (directory, file), 'feedback-in-db')
            shutil.move('%s/%s' % (directory, txt_file), 'feedback-in-db')

if __name__ == '__main__':
    manager.run()
