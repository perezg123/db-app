import flask
from flask import request, flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from .forms import OpportunityForm, ImplementationForm, oppstatus, opptype, regions, vendors
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from . import home
from .. import db
from ..models import Opportunity, Implementation, ListIndex, ListItems

def check_admin():
    """
    Prevent non-admins from accessing page
    """
    if not current_user.is_admin:
        abort(403)


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@home.route('/opportunities', methods=['GET', 'POST'])
@login_required
def list_opportunities():
    """
    List all opportunities
    """
    check_admin()
#    opportunities = Opportunity.query.all()
    qry = 'Select opportunities.oppid, b.name as opptype, a.name as status, c.name as region, ' \
          'createdate, ae, sa, am, customername, d.name as vendor, product, provider, description ' \
          'from opportunities inner join listitems as b on opportunities.opptype = b.id ' \
          'inner join listitems as a on opportunities.status = a.id ' \
          'inner join listitems as c on opportunities.region = c.id ' \
          'inner join listitems as d on opportunities.vendor = d.id'
    opportunities = db.session.execute(qry)
    return render_template('/home/opportunities/opportunities.html',
                        opportunities=opportunities, title="Opportunities")


@home.route('/opportunities/add/', methods=['GET', 'POST'])
@login_required
def add_opportunity():
    """
    Add an opportunity to the database
    """
    check_admin()
    add_opportunity = True
    form = OpportunityForm()
    if form.validate_on_submit():
        print (form.opptype.data)
        opptype = request.values.get('opptype')
        status = request.values.get('status')
        region = request.values.get('region')
        ae = request.values.get('ae')
        sa = request.values.get('sa')
        am = request.values.get('am')
        customername = request.values.get('customername')
        vendor = request.values.get('vendor')
        product = request.values.get('product')
        description = request.values.get('description')
        now = datetime.now()
        opportunity = Opportunity(oppid=None, opptype=opptype, status=status, createdate=now, region=region,
                                  ae=ae, sa=sa, am=am, customername=customername, vendor=vendor, product=product,
                                  description=description, provider=0)

        try:
            # add opportunity to the database
            db.session.add(opportunity)
            db.session.commit()
            oppid = opportunity.oppid
            if request.values.get('opptype') == '16':
                return redirect(url_for('home.add_implementation', id=oppid))

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            # redirect to opportunities page
            return redirect(url_for('home.list_opportunities'))

    flash_errors(form)
    # load opportunity template
    form=OpportunityForm()
    
    return render_template('home/opportunities/opportunity.html', action="Add",
            add_opportunity=add_opportunity, form=form, title="Add opportunity")


@home.route('/opportunities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id):
    """
    Edit a opportunity
    """
    check_admin()
    add_opportunity = False
    
    opportunity = Opportunity.query.get_or_404(id)
    form = OpportunityForm(obj=opportunity)
    if form.validate_on_submit():
        opp = form.oppid.data
        flash('You are editing an opportunity opp' + opp + '.')
        opportunity.oppid = form.oppid.data
        opportunity.customername = form.customername.data
        opportunity.description = form.description.data
        db.session.commit()
        # redirect to the opportunities page
        return redirect(url_for('home.list_opportunities'))

    form.description.data = opportunity.description
    form.customername.data = opportunity.customername
    return render_template('home/opportunities/opportunity.html', action="Edit",
                add_opportunity=add_opportunity, form=form, opportunity=opportunity, title="Edit opportunity")


@home.route('/opportunities/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_opportunity(id):
    """
    Delete a opportunity from the database
    """
    check_admin()
    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    flash('You have successfully deleted the opportunity.')

    # redirect to the opportunities page
    return redirect(url_for('home.list_opportunities'))

@home.route('/opportunities/implementations/', methods=['GET', 'POST'])
@login_required
def list_implementations():
    """
    List all implementations
    """
    check_admin()
    form=ImplementationForm()
    implementations = Implementation.query.all()
    return render_template('home/opportunities/implementations.html', form=form,
                           title="Implementations", implementations=implementations)


@home.route('/opportunities/implementation/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_implementation(id):
    """
    Insert a new implementation opp with base opp id
    """
    check_admin()
    implementation = Implementation.query.get(id)
    form=ImplementationForm(obj=implementation)
    if form.is_submitted():
        if len(request.values.get('req_sent_date')) <= 0:
            req_sent_date = None
        else:
            req_sent_date = request.values.get('req_sent_date')
        if len(request.values.get('req_resp_date')) <= 0:
            req_resp_date = None
        else:
            req_resp_date = request.values.get('req_resp_date')
        if len(request.values.get('scopingcall_sched_date')) <= 0:
            scopingcall_sched_date = None
        else:
            scopingcall_sched_date = request.values.get('scopingcall_sched_date')
        if len(request.values.get('scopingcall_comp_date')) <= 0:
            scopingcall_comp_date = None
        else:
            scopingcall_comp_date = request.values.get('scopingcall_comp_date')
        if len(request.values.get('tpp_sow_received_date')) <= 0:
            tpp_sow_received_date = None
        else:
            tpp_sow_received_date = request.values.get('tpp_sow_received_date')
        if len(request.values.get('tpp_submit_date')) <= 0:
            tpp_submit_date = None
        else:
            tpp_submit_date = request.values.get('tpp_submit_date')
        if len(request.values.get('pp_complete_date')) <= 0:
            pp_complete_date = None
        else:
            pp_complete_date = request.values.get('pp_complete_date')
        if len(request.values.get('approval1_date')) <= 0:
            approval1_date = None
        else:
            approval1_date = request.values.get('approval1_date')
        if len(request.values.get('approval2_date')) <= 0:
            approval2_date = None
        else:
            approval2_date = request.values.get('approval2_date')
        if len(request.values.get('sow_reviewed_date')) <= 0:
            sow_reviewed_date = None
        else:
            sow_reviewed_date = request.values.get('sow_reviewed_date')
        if len(request.values.get('sow_to_cust_date')) <= 0:
            sow_to_cust_date = None
        else:
            sow_to_cust_date = request.values.get('sow_to_cust_date')
        if len(request.values.get('cust_approved_date')) <= 0:
            cust_approved_date = None
        else:
            cust_approved_date = request.values.get('cust_approved_date')
 #   if form.validate_on_submit():

        try:
            implementation = Implementation(oppid=id,
                                            description=request.values.get('description'),
                                            opp_status=request.values.get('status'), provider=request.values.get('provider'),
                                            req_sent_date = req_sent_date, req_resp_date = req_resp_date,
                                            scopingcall_sched_date = scopingcall_sched_date,
                                            scopingcall_comp_date = scopingcall_comp_date,
                                            tpp_sow_received_date = tpp_sow_received_date,
                                            tpp_submit_date = tpp_submit_date, pp_complete_date = pp_complete_date,
                                            approval1_date = approval1_date, approval2_date = approval2_date,
                                            sow_reviewed_date = sow_reviewed_date, sow_to_cust_date = sow_to_cust_date,
                                            cust_approved_date=cust_approved_date
                                            )
            db.session.add(implementation)
            db.session.commit()
            flash('Implementation Created.')
            return render_template('home/opportunities/implementations.html',
                                   add_implementation=False, form=form, title="Implementations")
        except SQLAlchemyError as e:
            print(form.errors.items)
            flash('Error: details could not be created.')
            error = str(e.__dict__['orig'])
            flash(error)
            # redirect to opportunities page
            return redirect(url_for('home.list_opportunities'))

    return render_template('home/opportunities/implementation.html', form=form,
                           title="Implementation Details", data=implementation, id=id)

@home.route('/opportunities/implementation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_implementation(id):
    """
    Edit an implementation
    """
    check_admin()
    add_implementation = False

    implementation = Implementation.query.get_or_404(id)
    form = OpportunityForm(obj=implementation)
    if form.validate_on_submit():
        id = form.id.data
        oppid = form.oppid.data
        flash('You are editing implementation ' + id + '.')
        implementation.id = form.id.data
        implementation.customername = form.customername.data
        implementation.description = form.description.data
        db.session.commit()
        # redirect to the implementation page
        return redirect(url_for('home.list_implementations'))

    form.description.data = implementation.description
    form.customername.data = implementation.customername
    return render_template('home/opportunities/implementations.html', action="Edit",
                           add_implementation=add_implementation, form=form, implementation=implementation,
                           title="Edit Implementation")

@home.route('/opportunities/implementation/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_implementation(id):
    """
    Delete an implementation from the database
    """
    check_admin()
    implementation = Implementation.query.get_or_404(id)
    db.session.delete(implementation)
    db.session.commit()
    flash('You have successfully deleted the implementation.')

    # redirect to the implementations page
    return redirect(url_for('home.list_implementations'))

@home.route('/dashboard')
@login_required
def dashboard():
    data = db.session.execute("select * from opportunities")
            
    if data is None:
        return "There are no current opportunities."
    else:
        """
        Render the dashboard template on the /dashboard route
        """
        return render_template('home/opportunities/opportunities.html', title="Opportunities", data=data)


