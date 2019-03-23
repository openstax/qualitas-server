import requests
from flask import current_app as app, abort
from flask_security import UserMixin, RoleMixin

from ..core import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    extend_existing=True
)


class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

    def __repr__(self):
        return self.name


class GitHubUser(db.Model):
    __tablename__ = 'github_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String, nullable=False)
    profile_link = db.Column(db.String, nullable=False)

    @classmethod
    def gh_load(cls, username, update=True):

        user = cls.query.filter(cls.username == username).first()

        if user is None:
            user = User()
            user.gh_update(username)
        elif update or user.display_name is None:
            user.gh_update(username)

        return user

    def gh_update(self, username, data=None):
        if data is None:
            client = app.github.client
            data = client.user(username)
            
        if data:
            self.id = data.id
            self.display_name = data.login
            self.username = data.login
            self.profile_image = data.avatar_url
            self.profile_link = data.html_url
            self.active = True
        else:
            # Create a dummy user if there is no data
            self.id = 1234
            self.display_name = 'user1234'
            self.username = 'user1234'
            self.profile_image = ''
            self.profile_link = ''
            self.is_active = True
            
        return self


class User(UserMixin, GitHubUser):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.ForeignKey(GitHubUser.id), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @classmethod
    def get(cls, user_id):
        return db.session.query(cls).get(user_id)

    @classmethod
    def oauth_load(cls, token):

        headers = {
            'Authorization': 'token {}'.format(token)
        }

        r = requests.get('https://api.github.com/user', headers=headers)
        if r.status_code == 200:
            data = r.json()
            user = User.query.filter(User.id == data['id']).first()

            if user is None:
                user = User(id=data['id'],
                            username=data['login'],
                            display_name=data['login'],
                            profile_image=data['avatar_url'],
                            profile_link=data['html_url'],
                            active=True)
                db.session.add(user)
                db.session.commit()
                return user
            else:
                return user

        else:
            abort(404)

