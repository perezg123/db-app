from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, SubmitField, SelectField, TextAreaField, DateTimeField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Opportunity, Implementation, StatusCodes, ListIndex, Vendors, Products, Partners, ListItems
from .. import db

def _required(form, field):
    if not field.data or not field.data[0]:
        raise ValidationError('Field is required!')

def oppstatus():
    return ListItems.query.filter_by(listindex_id=18)

def opptype():
    return ListItems.query.filter_by(listindex_id=19)

def regions():
    return ListItems.query.filter_by(listindex_id=17)

class ListsForm(FlaskForm):
    list_name = SelectField('List Name')
    submit = SubmitField('Edit')

class OpportunityForm(FlaskForm):
    """
    Form to add or edit an opportunity
    """
    oppid = HiddenField()
    status = QuerySelectField('Status', query_factory=oppstatus, get_label='itemname', validators=[DataRequired()])
    opptype = QuerySelectField('Opportunity Type', query_factory=opptype, get_label='itemname', validators=[DataRequired()])
    customername = StringField('Customer', validators=[DataRequired()])
    region = QuerySelectField('Sales Region', query_factory=regions, get_label='itemname',  validators=[DataRequired()])
    ae = StringField('Account Exec', validators=[DataRequired()])
    sa = StringField('Solutions Architect', validators=[DataRequired()])
    asm = StringField('Area Security Manager', validators=[DataRequired()])
    vendor = SelectField('Product Vendor', choices=[(1, 'Cisco'), (2, 'Palo Alto'), (3, 'Fortinet'), (4, 'Symantec'), (5, 'McAfee'), (6, 'Sophos'), (7, 'Other')], validators=[DataRequired()])
    product = StringField('Security Product', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Opportunity')

class ImplementationForm(FlaskForm):
    """
    Form for implementations
    """
    description = TextAreaField('Description')
    provider = StringField('Service Provider', validators=[DataRequired()])
    req_sent_date = DateTimeField('Request Sent')
    req_resp_date = DateTimeField('Response Received')
    scopingcall_sched_date = DateTimeField('Scoping Call Scheduled')
    scopingcall_comp_date = DateTimeField('Scoping Call Completed')
    tpp_sow_received_date = DateTimeField('3rd Party SoW Received')
    tpp_submit_date = DateTimeField('3rd Party SoW Submitted')
    pp_complete_date = DateTimeField('3rd Party SoW Transferred')
    approval1_date = DateTimeField('1st Approval Complete')
    approval2_date = DateTimeField('2nd Approval Complete')
    sow_reviewed_date = DateTimeField('SoW Reviewed')
    sow_to_cust_date = DateTimeField('SoW to Customer')
    cust_approved_date = DateTimeField('Customer Signed SoW')
    opp_status = SelectField('Opportunity Status', choices=[('1', 'Initial'), ('2', 'Qualified'), ('3', 'Seeking Provider'), ('4', 'Pending Scope Call'), ('5', 'Pending SoW'), ('6', 'Pending Exec Approval'), ('7', 'SoW Delivered'), ('8', 'Cust Signed'), ('9', 'Executed'), ('10', 'Kick-off'), ('11', 'In Progress'), ('12', 'Delayed'), ('13', 'Completed'), ('14', 'Closd Lost'), ('15', 'Closed Delivered')], validators=[DataRequired()])
    date_closed = DateTimeField('Opportunity Closed')
    submit = SubmitField('Save')

class AddOppForm(FlaskForm):
    """
    Form for creating new opportunities
    """
    opptype = SelectField('Opportunity Type', choices=[('Implementation', 'Implementation'), ('Consulting', 'Consulting'), ('Pre-sales', 'Pre-sales'), ('Demo', 'Demo')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('1', 'Initial'), ('2', 'Qualified'), ('3', 'Seeking Provider'), ('4', 'Pending Scope Call'), ('5', 'Pending SoW'), ('6', 'Pending Exec Approval'), ('7', 'SoW Delivered'), ('8', 'Cust Signed'), ('9', 'Executed'), ('10', 'Kick-off'), ('11', 'In Progress'), ('12', 'Delayed'), ('13', 'Completed'), ('14', 'Closd Lost'), ('15', 'Closed Delivered')], validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    region = SelectField('Sales Region', choices=[('West', 'West'), ('Central', 'Central'), ('East', 'East'), ('Gov', 'Gov')], validators=[DataRequired()])
    ae = StringField('Account Exec', validators=[DataRequired()])
    sa = StringField('Solutions Architect', validators=[DataRequired()])
    asm = StringField('Area Security Manager', validators=[DataRequired()])
    vendor = SelectField('Product Vendor', choices=[('Cisco', 'Cisco'), ('Palo Alto', 'Palo Alto'), ('Fortinet', 'Fortinet'), ('Symantec', 'Symantec'), ('McAfee', 'McAfee'), ('Sophos', 'Sophos')], validators=[DataRequired()])
    product = StringField('Security Product', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add')

class EditOppForm(FlaskForm):
    """
    Form for editing opportunities
    """

    opptype = SelectField('Opportunity Type', choices=[('Implementation', 'Implementation'), ('Consulting', 'Consulting'), ('Pre-sales', 'Pre-sales'), ('Demo', 'Demo')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('1', 'Initial'), ('2', 'Qualified'), ('3', 'Seeking Provider'), ('4', 'Pending Scope Call'), ('5', 'Pending SoW'), ('6', 'Pending Exec Approval'), ('7', 'SoW Delivered'), ('8', 'Cust Signed'), ('9', 'Executed'), ('10', 'Kick-off'), ('11', 'In Progress'), ('12', 'Delayed'), ('13', 'Completed'), ('14', 'Closd Lost'), ('15', 'Closed Delivered')], validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    region = SelectField('Sales Region', choices=[('West', 'West'), ('Central', 'Central'), ('East', 'East'), ('Gov', 'Gov')], validators=[DataRequired()])
    ae = StringField('Account Exec', validators=[DataRequired()])
    sa = StringField('Solutions Architect', validators=[DataRequired()])
    asm = StringField('Area Security Manager', validators=[DataRequired()])
    vendor = SelectField('Product Vendor', choices=[('Cisco', 'Cisco'), ('Palo Alto', 'Palo Alto'), ('Fortinet', 'Fortinet'), ('Symantec', 'Symantec'), ('McAfee', 'McAfee'), ('Sophos', 'Sophos')], validators=[DataRequired()])
    product = StringField('Security Product', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add')

