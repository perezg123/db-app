import flask
from flask import request, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from .forms import AddOppForm, EditOppForm, OpportunityForm
from datetime import datetime

from . import home
from .. import db
from ..models import Opportunity, Implementation, ListIndex, ListItems

def check_admin():
    """
    Prevent non-admins from accessing page
    """
    if not current_user.is_admin:
        abort(403)

@home.route('/opportunities', methods=['GET', 'POST'])
@login_required
def list_opportunities():
    """
    List all opportunities
    """
    check_admin()
    opportunities = Opportunity.query.all()                    
    return render_template('home/opportunities/opportunities.html',
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
    print(request.values.get('opptype'), flush=True)
    if form.validate_on_submit():
        abort(403)
        opptype = format(form.opptype.data)
        now = datetime.now()
        opportunities = Opportunity(opptype=form.opptype.data, status=form.status.data, 
                createdate=now, region=form.region.data, 
                ae=form.ae.data, sa=form.sa.data, am=form.asm.data, 
                customername=form.customername.data, 
                vendor=form.vendor.data, product=form.product.data, 
                description=form.description.data) 
        try:
            # add opportunity to the database
            db.session.execute(opportunities)
            db.session.commit()
            oppid = opportunities.lastrowid
            if opptype == 1:
                try:
                    implementation = Implementation(oppid, 
                            description=form.description.data, opp_status=form.status.data)
                    db.session.add(implementation)
                    db.session.commit()
                    flash('Opportunity Created. Please add implementation details.')
                    return redirect(url_for('home.opportunities.add_implementation'),oppid=oppid)
                except:
                    flash('Error: the opportunity details could not be added.')

        except:
            # in case opportunity name already exists
            flash('Error: unable to add or opportunity name already exists.')

            # redirect to opportunities page
            return redirect(url_for('home.list_opportunities'))

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

    return render_template(title="Delete opportunity")

@home.route('/opportunities/implementation/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_implementation(id):
    """
    Insert a new implementation opp with base opp id
    """
    check_admin()
    if form.validate_on_submit():
        implementation = Implementation.query.get(id)
    else:
        return render_template(title="Implementation Opportunity")

    return render_template(form='ImplementationForm', title="Implementation Details", 
                            data=implementation, id=id)

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
            return render_template('home/dashboard.html', title="Dashboard", data=data)


