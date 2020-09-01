from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required

from sampling import db
from sampling.models import Html
from sampling.page.forms import HtmlForm

import random
import string

page = Blueprint('page', __name__)

def get_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

#LIST
@page.route('/pages', methods=['GET'])
@login_required
def list_pages():
    htmls = Html.query.filter_by(user_id=current_user.id).order_by(Html.date.desc()).all()
    return render_template('/page_list.html', htmls=htmls)

# CREATE
@page.route('/page/create', methods=['GET', 'POST'])
@login_required
def create_page():

    form = HtmlForm()

    action = request.form.get("copy_text_action")
    if action == "1":
        copy_text = request.form.get("copy_text")
        form.html.data = copy_text
    elif form.validate_on_submit():
        html = Html(html_key=form.html_key.data, html=form.html.data, user_id=current_user.id)
        
        html_words = html.html.split(" ")
        cc_words = len(html_words)

        new_html = ""
        if cc_words > 96:
            cc_words = 96
        for i in range(cc_words):
            new_html = new_html + html_words[i] + " "

        cc_chars = len(new_html[0:-1])
        if cc_chars > 1156:
            new_html = new_html[0: 1156]

        html.html = new_html

        db.session.add(html)
        db.session.commit()
        return redirect(url_for('page.list_pages'))

    form.html_key.data = get_random_string(16)

    return render_template('create_page.html', form=form, page_name="New Page")

# VIEW
@page.route('/page/view/<html_key>')
def view_html(html_key):
    html = Html.query.filter_by(html_key=html_key).first_or_404()  

    return render_template('page_view.html', html=html)


# Edit Comment
@page.route('/page/edit/<html_key>', methods=['GET', 'POST'])
@login_required
def update_page(html_key):
    html = Html.query.filter_by(html_key=html_key).first_or_404()  
    
    form = HtmlForm()

    if form.validate_on_submit():
        html.html = form.html.data

        html_words = html.html.split(" ")
        cc_words = len(html_words)

        print(cc_words)

        new_html = ""
        if cc_words > 96:
            cc_words = 96
        for i in range(cc_words):
            new_html = new_html + html_words[i] + " "

        cc_chars = len(new_html[0:-1])
        print(cc_chars)
        if cc_chars > 1156:
            new_html = new_html[0: 1156]

        html.html = new_html

        db.session.commit()
        return redirect(url_for('page.list_pages'))

    # Populate the data to the field
    form.html_key.data = html.html_key
    form.html.data = html.html
    return render_template('create_page.html', form=form)


# Delete html
@page.route('/page/delete/<html_key>', methods=['GET', 'POST'])
@login_required
def delete_page(html_key):
    html = Html.query.filter_by(html_key=html_key).first_or_404()    
    db.session.delete(html)
    db.session.commit()
    return redirect(url_for('page.list_pages'))

@page.route('/', methods=['GET', 'POST'])
def index():
    return redirect("/pages")

