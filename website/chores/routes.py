""" All routes related to chores and chore assignment. """

from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from website.chores.utils import chore_sorting
from website import db
from website.models import Tasks
from flask_login import current_user
from datetime import timedelta, datetime as dt
import json
from pathlib import Path


chores = Blueprint('chores', __name__)


@chores.route('/chore')
def chore() -> str:
    """ The route to display the chores assigned. """
    if current_user.is_parent:
        tasks = Tasks.query.filter(Tasks.date >= (dt.today() + timedelta(days=-1))).all()
    else:
        tasks = Tasks.query.filter_by(user_id=current_user.id, is_active=True)
    return render_template('chore.html', user=current_user, tasks=tasks)


@chores.route('/delete-chore', methods=['POST'])
def delete_task():
    """ Marking a chore completed. """
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Tasks.query.get(task_id)
    if task:
        if task.user_id == current_user.id or current_user.is_parent:
            task.is_active = False
            db.session.commit()
    return jsonify({})


@chores.route('/get-chores')
def get_chores():
    """ Obtain a new set of chores for the day, only accessible from the admin menu. """
    database = str(Path(__file__).parent.parent) + '/database.db'
    chore_sorting(database)
    return redirect(url_for('chores.chore'))
