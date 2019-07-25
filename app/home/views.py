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
    print form.errors.items()
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


@home.route('/opportunities/implementation/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_implementation(id):
    """
    Insert a new implementation opp with base opp id
    """
    check_admin()
    implementation = Implementation.query.get(id)
    form=ImplementationForm(obj=implementation)
    if form.validate_on_submit():
        try:
            implementation = Implementation(oppid=oppid,
                                            description=request.values.get('description'),
                                            opp_status=request.values.get('status'))
            db.session.add(implementation)
            db.session.commit()
            flash('Implementation Created.')
            return render_template('home/opportunities/implementations.html',
                                   add_implementation=False, form=form, title="Implementations")
        except:
            print form.errors.items()
            flash_errors()
            flash('Error: details could not be created.')

    return render_template('home/opportunities/implementation.html', form=form,
                           title="Implementation Details", data=implementation, id=id)

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
                           title="Implementations", data=implementations)


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


