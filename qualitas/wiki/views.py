import logging

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for, flash)
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from qualitas.factory import db
from qualitas.wiki.models import WikiPage

from .forms import CreateWikiForm, EditWikiForm

LOGS = logging.getLogger(__name__)

wiki = Blueprint('wiki',
                 __name__,
                 template_folder='../templates/wiki')


@wiki.route('/', methods=['GET'])
def index():
    wiki_pages = WikiPage.query.order_by(WikiPage.updated.desc())

    if not current_user.is_authenticated:
        wiki_pages = wiki_pages.filter(db.and_(
            WikiPage.public == True, WikiPage.draft == False))
    else:
        # Subquery needed to hide non-user draft pages
        non_user_pages = WikiPage.query.filter(db.and_(
            WikiPage.author_id != current_user.id,
            WikiPage.draft == True)).with_entities(WikiPage.id).subquery()

        wiki_pages = wiki_pages.filter(
            ~WikiPage.id.in_(non_user_pages))

    return render_template('index.html', wiki_pages=wiki_pages)


@wiki.route('/create', endpoint='create', methods=['GET', 'POST'])
@wiki.route('/<wiki_title:title>/update', methods=['GET', 'POST'])
@login_required
def update(title=None):
    page = WikiPage.query.filter(
        WikiPage.title == title).first_or_404() if title is not None else None

    if page:
        form = EditWikiForm(obj=page)
    else:
        form = CreateWikiForm()
    if form.validate_on_submit():
        if page is None:
            page = WikiPage()
            page.author = current_user
        page.last_updated_by = current_user
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
@login_required
def delete(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()
    form = FlaskForm()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        return redirect(url_for('wiki.index'))
    return render_template('delete.html', page=page, form=form)
