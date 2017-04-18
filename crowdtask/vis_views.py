import re
import random
import string
import json
from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery

vis_views = Blueprint('vis_views', __name__, template_folder='templates')

@vis_views.route('/ensemble_vis/<feedback_id>', methods=('GET','POST'))
def ensemble_vis(feedback_id):

    verified_string = generate_verified_str(6)
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
        "article_content": article_content,
        "feedback_content": json.dumps(feedback_content),
        
        "verified_string": verified_string
    }

    return render_template('ensemble_vis.html', data=data)


def generate_verified_str(number):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(number))