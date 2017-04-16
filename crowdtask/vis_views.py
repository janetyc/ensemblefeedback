import re
import random
import string
from flask import Blueprint, Flask, request, render_template, redirect, url_for, jsonify
from crowdtask.dbquery import DBQuery

vis_views = Blueprint('vis_views', __name__, template_folder='templates')

@vis_views.route('/ensemble_vis', methods=('GET','POST'))
def ensemble_vis():
    data = {

    }
    return render_template('ensemble_vis.html', data=data)
