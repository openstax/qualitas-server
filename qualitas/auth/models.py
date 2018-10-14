from flask_security import UserMixin, RoleMixin

from ..core import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


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
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    display_name = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String, nullable=False)
    profile_link = db.Column(db.string, nullable=False)

    @classmethod
    def gh_load(cls, ident, update=True):

        o = cls.get_unique(id=id)

        if update or o.display_name is None:
            o.gh_update()

        return o

    def gh_update(self, data=None):
        if data is None:
            pass


class User(UserMixin, GitHubUser):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.ForeignKey(GitHubUser.id), primary_key=True)
    active = db.Column(db.Boolean())
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
