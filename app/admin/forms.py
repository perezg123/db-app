from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, StringField, SubmitField, SelectField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Employee, Contact, ListIndex

class ListsForm(FlaskForm):
    """
    Form to create and edit lists
    """
    listname = StringField('List Name')
    listdescr = StringField('List Description')
    submit = SubmitField('Submit')

class ListItemsForm(FlaskForm):
    """
    Form to add items to lists
    """
    listindex = IntegerField('List Number')
    itemindex = IntegerField('Item Index')
    itemname = StringField('Item Name')
    itemdescr = StringField('Item Description')
    listname = HiddenField()
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    """
    Form to add and edit contacts
    """
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Add')

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(), get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    submit = SubmitField('Submit')


