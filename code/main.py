from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from flask_bootstrap import Bootstrap

import database_connection
import recommendation as rec

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'XduazXx967oD1W38EB8P'

users = database_connection.get_all_users_ids()

class FileListFormBase(FlaskForm):
    submit = SubmitField('Submit')

def file_list_form_builder(users):
    class FileListForm(FileListFormBase):
        pass

    for id in users:
        setattr(FileListForm, f"user_{id}", BooleanField(label=f"user {id}"))

    return FileListForm()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = file_list_form_builder(users)
    if request.method == 'POST':
        # a list of choosen users
        users_checked = list(request.form)
        users_checked.remove('submit')
        session['users_checked'] = users_checked
        return redirect(url_for('recommendation'))

    return render_template('index.html', form=form, users=users)

@app.route('/recommendation')
def recommendation():
    users_checked = session['users_checked']

    users_ids = [int(user.replace('user_', '')) for user in users_checked]
    
    recommendation_df = rec.make_recommendation(users_ids)

    df_html = recommendation_df.to_html(justify='left', classes="table table-striped")

    return render_template('recommendation.html', df_html=df_html)

if __name__ == '__main__':
    app.run(debug=True)