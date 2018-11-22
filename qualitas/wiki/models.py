from datetime import datetime

from flask import url_for
from qualitas.auth.models import User

from qualitas.factory import db


class WikiPage(db.Model):
    __tablename__ = 'wiki_page'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column('title', db.String, nullable=False, unique=True)
    text = db.Column(db.String, nullable=False)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    public = db.Column(db.Boolean, nullable=False, default=False)
    draft = db.Column(db.Boolean, nullable=False, default=False)
    redirect_id = db.Column(db.Integer, db.ForeignKey('wiki_page.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship(User, foreign_keys=[author_id])
    last_updated_by = db.relationship(User, foreign_keys=[last_updated_by_id])

    def __str__(self):
        return self.title

    @property
    def detail_url(self):
        return url_for('wiki.detail', title=self.title)

    @property
    def update_url(self):
        return url_for('wiki.update', title=self.title)

    @property
    def delete_url(self):
        return url_for('wiki.delete', title=self.title)
