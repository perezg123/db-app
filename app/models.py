from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)
 

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
		
class Opportunity(db.Model):
    """
    Create the Opportunity table
    """

    __tablename__ = 'opportunities'

    oppid = db.Column(db.Integer, primary_key=True)
    opptype=db.Column(db.Integer)
    status=db.Column(db.Integer)
    createdate=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    region=db.Column(db.Integer)
    ae=db.Column(db.String(60))
    sa=db.Column(db.String(60))
    am=db.Column(db.String(60))
    customername=db.Column(db.String(120),index=True)
    vendor=db.Column(db.Integer)
    product=db.Column(db.Integer)
    description=db.Column(db.String(200))
    provider=db.Column(db.Integer)
    implementations = db.relationship('Implementation', back_populates='opportunity')
                                                                
    def __repr__(self):
        return '<Opportunity: {}>'.format(self.name)

class Implementation(db.Model):

    __tablename__ = 'implementation'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    oppid = db.Column(db.Integer, db.ForeignKey('opportunities.oppid'))
    opportunity = db.relationship('Opportunities', back_populates('implementation'))
    description = db.Column(db.String(120))
    provider = db.Column(db.Integer)
    req_sent_date = db.Column(db.DateTime, index=True)
    req_resp_date = db.Column(db.DateTime, index=True)
    scopingcall_sched_date = db.Column(db.DateTime, index=True)
    scopingcall_comp_date = db.Column(db.DateTime, index=True)
    tpp_sow_received_date = db.Column(db.DateTime, index=True)
    tpp_submit_date = db.Column(db.DateTime, index=True)
    pp_complete_date = db.Column(db.DateTime, index=True)
    approval1_date = db.Column(db.DateTime, index=True)
    approval2_date = db.Column(db.DateTime)
    sow_reviewed_date = db.Column(db.DateTime)
    sow_to_cust_date = db.Column(db.DateTime)
    cust_approved_date = db.Column(db.DateTime)
    opp_status = db.Column(db.Integer)
    date_closed = db.Column(db.Integer)

    def __repr__(self):
        return '<Implementation: {}>'.format(self.name)

class StatusCodes(db.Model):
    """
    Create StatusCodes table
    """
		
    __tablename__='statuscodes'
		
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60),index=True)
    listkey=db.Column(db.Integer)
		
    def __repr__(self):
        return '<StatusCodes: {}>'.format(self.name)				

class ListItems(db.Model):
    """
    Create List Items Table
    """

    __tablename__='listitems'
    
    id=db.Column(db.Integer,primary_key=True)
    listindex_id=db.Column(db.Integer, db.ForeignKey('listindex.id'))
    itemname=db.Column(db.String(60))
    itemdescr=db.Column(db.String(60))
    itemindex=db.Column(db.Integer)

    def __repr__(self):
        return '<ListItems: {}>'.format(self.name)
		
class ListIndex(db.Model):
    """
    Create List Key table
    """
		
    __tablename__='listindex'
		
    id=db.Column(db.Integer, index=True, primary_key=True)
    listname=db.Column(db.String(60))
    listid=db.Column(db.Integer)
    listdescr=db.Column(db.String(60))
    items=db.relationship('ListItems', backref='listindex', lazy='dynamic')
		
    def __repr__(self):
        return '<ListIndex: {}>'.format(self.name)
		
class Vendors(db.Model):
    """
    Create Vendors table
    """
	
    __tablename__="vendors"
	
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60),index=True)
    tier=db.Column(db.Integer)
	
    def __repr__(self):
        return '<ListKey: {}>'.format(self.name)
	

class Products(db.Model):	
    """
    Create Products table
    """
	
    __tablename__="products"
	
    id=db.Column(db.Integer,primary_key=True)
    product=db.Column(db.String(120),index=True)
    vendorid=db.Column(db.Integer)

    def __repr__(self):
        return '<Products: {}>'.format(self.name)
	

class Partners(db.Model):
    """
    Create Partners Table
    """
	
    __tablename__="partners"
	
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),index=True)
    street1=db.Column(db.String(60))
    street2=db.Column(db.String(60))
    city=db.Column(db.String(20))
    state=db.Column(db.String(2))
    zip=db.Column(db.Integer)
	
    def __repr__(self):
        return '<Partners: {}>'.format(self.name)	
	
	
class MapProductPartner(db.Model):
    """
    Create PartnerProduct mapping table
    """
	
    __tablename__="mapproductpartner"
	
    id=db.Column(db.Integer,primary_key=True)
    productid=db.Column(db.Integer)
    vendorid=db.Column(db.Integer)
	
    def __repr__(self):
        return '<MapProductPartner: {}>'.format(self.name)	
	
	
class Contact(db.Model):
    """
    Create Contacts table
    """
	
    __tablename__="contacts"
    __table_args__ = {'extend_existing': True}
	
    id=db.Column(db.Integer,primary_key=True)
    first=db.Column(db.String(60),index=True)
    last=db.Column(db.String(60),index=True)
    title=db.Column(db.String(60))
    email=db.Column(db.String(120),index=True)
    phone=db.Column(db.Integer)
    company=db.column(db.String(60))
    listkey=db.Column(db.Integer)
	
    def __repr__(self):
        return '<Contact: {}>'.format(self.name)		
	
	
	
