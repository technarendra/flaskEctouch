from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import Table, Column, String, Integer, Float, DateTime, ForeignKey, Boolean

from app import db, login
from sqlalchemy.dialects.postgresql import JSON

from app import db


# Bind users and organizations
users_orgs_association_table = db.Table("users_orgs_association",
                                        db.Column("org_id",
                                                  db.Integer,
                                                  db.ForeignKey("organizations.id", ondelete="CASCADE")),
                                        db.Column("user_id",
                                                  db.Integer,
                                                  db.ForeignKey("users.id", ondelete="CASCADE")))


class User(UserMixin, db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64))
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=False)
	organizations = db.relationship("Organization",
		                            secondary=users_orgs_association_table,
		                            back_populates="users")

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)



@login.user_loader
def load_user(id):
	user_id = db.session.query(User).get(int(id))

	return user_id


class Organization(db.Model):
	__tablename__ = "organizations"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, index=True)
	data_dir = db.Column(db.String(200), unique=True, index=True)
	users = db.relationship("User",
							secondary=users_orgs_association_table,
							back_populates="organizations")
	clerks = db.relationship("Clerk", cascade="delete")
	customers = db.relationship("Customer", cascade="delete")
    




class Order(db.Model):
	__tablename__ = "orders"

	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.String(50))
	table_number = db.Column(db.Integer)
	clerk_id = db.Column(db.Integer)
	customer_id = db.Column(db.Integer)
	consecutive_number = db.Column(db.Integer)
	cover = db.Column(db.String(50))
	status = db.Column(db.String(50))
	mode = db.Column(db.String(50))

	def __repr__(self):
		return "Order: ID=%s" % (self.id)



class Clerk(db.Model):
	__tablename__ = "clerks"

	id = db.Column(db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True )
	name = db.Column(db.String(50))
	def __repr__(self):
		return "Clerk: id=%s name=%s" % (self.number, self.name)

		

class Customer(db.Model):
	__tablename__ = "customers"

	id = db.Column(db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True )
	first_name = db.Column(db.String(50))
	surname = db.Column(db.String(50))
	addr1 = db.Column(db.String(100))

	def __repr__(self):
		return "Customer: id=%s first_name=%s surname=%s surname=%s" % (self.id, self.first_name, self.surname, self.addr1)
