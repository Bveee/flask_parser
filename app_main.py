import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from settings import DEBUG, ROWS_PER_PAGE

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from utils import history_id, update_db, view_db


@app.route('/smartphones', methods=['GET'], defaults={"page": 1})
@app.route('/smartphones/page-<int:page>', methods=['GET'])
def view(page):
    return render_template(
        'smartphones.html',
        title='Wildberries',
        my_list=view_db(page),
        page=page,
        per_page=ROWS_PER_PAGE
        )


@app.route('/smartphones/<int:id>', methods=['GET'])
def details(id):
    return render_template(
        'details.html',
        title=id,
        my_list=history_id(id)
        )


@app.route('/smartphones/update')
def save_dict():
    update_db(1)
    return render_template(
        'update_db.html',
        )


if __name__ == '__main__':
    app.run(DEBUG)
