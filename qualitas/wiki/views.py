import logging

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for, flash)
from flask_wtf import FlaskForm

from qualitas.factory import db
from qualitas.wiki.models import WikiPage

from .forms import CreateWikiForm, EditWikiForm

LOGS = logging.getLogger(__name__)

wiki = Blueprint('wiki',
                 __name__,
                 url_prefix='/wiki',
                 template_folder='../templates/wiki')


@wiki.route('/', methods=['GET'])
def index():
    wiki_pages = WikiPage.query.all()

    return render_template('index.html', wiki_pages=wiki_pages)

# @wiki.route('/create', endpoint='create', methods=['GET', 'POST'])
# @wiki.route('/<wiki_title:title>/update', methods=['GET', 'POST'])
# def update(title=None):
#     # Pick the proper form bas

@wiki.route('/create', endpoint='create', methods=['GET', 'POST'])
@wiki.route('/<wiki_title:title>/update', methods=['GET', 'POST'])
def update(title=None):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404() if title is not None else None

    if page:
        form = EditWikiForm(obj=page)
    else:
        form = CreateWikiForm()
    if form.validate_on_submit():
        if page is None:
            page = WikiPage()
            db.session.merge(page)
        form.populate_obj(page)
        db.session.merge(page)
        db.session.commit()
        return redirect(page.detail_url)
    return render_template('create.html', form=form)


@wiki.route('/<wiki_title:title>', methods=['GET'])
def detail(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()

    return render_template('detail.html', page=page)


@wiki.route('<wiki_title:title>/delete', methods=['GET', 'POST'])
def delete(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()
    form = FlaskForm()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        return redirect(url_for('wiki.index'))
    return render_template('delete.html', page=page, form=form)


