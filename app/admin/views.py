from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from . import admin
from .forms import ContactForm, ListsForm, ListItemsForm, DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Employee, Department, Role, Contact, ListIndex, ListItems

def check_admin():
    """
    Prevent non-admins from accessing page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html', 
    				employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()
    employee = Employee.query.get_or_404(id)
    # prevent admin from being assigned a department or role
    if employee.is_admin:
            abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees.html', employee=employee, 
        				form=form, title='Assign Employee'))

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles=Role.query.all()
    return render_template('/admin/roles/roles.html', roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()
    add_role = True
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)
        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')
        #redirect to roles page
        return redirect(url_for('admin.list_roles'))
    
    return render_template('/admin/roles/role.html', add_role=add_role,
    				form=form, title='Add Role')

@admin.route('roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()
    add_role=False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        #redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role, 
    				form=form, title='Edit Role')

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    #redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()
    departments = Department.query.all()                    
    return render_template('admin/departments/departments.html',
                        departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
            add_department=add_department, form=form, title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()
    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')
        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                    add_department=add_department, form=form, 
                    department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

@admin.route('/contacts', methods=['GET', 'POST'])
@login_required
def list_contacts():
    """
    List all contacts
    """
    contacts=Contact.query.all()
    return render_template('/admin/contacts/contacts.html', 
    			contacts=contacts, title='Contacts')

@admin.route('/contacts/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    """
    Add a contact to the database
    """
    check_admin()
    add_contact = True
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(first=form.first.data, last=form.last.data, 
        			title=form.title.data, company=form.company.data, 
        			phone=form.phone.data, email=form.email.data)
        try:
            db.session.add(contact)
            db.session.commit()
            flash('You have added the new contact.')
        except:
            flash('Error: the contact could not be added.')
        return redirect(url_for('admin.list_contacts'))
    return render_template('admin/contacts/contact.html', action="Add", 
    				add_contact=add_contact, form=form, title='Add Contact')

@admin.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contacts():
    form = ContactForm(obj=contact)

    return render_template('auth/contacts/contact.html', form=form, title='Contacts')

@admin.route('/lists', methods=['GET', 'POST'])
@login_required
def list_lists():
    form = ListsForm()
    lists = ListIndex.query.all()

    return render_template('admin/lists/lists.html', form=form, 
    				title='Manage Lists', lists=lists)


@admin.route('/lists/add', methods=['GET', 'POST'])
@login_required
def add_list():
    """
    Add a role to the database
    """
    check_admin()
    add_list = True
    form = ListsForm()
    if form.validate_on_submit():
        list = ListIndex(listname=form.listname.data, listdescr=form.listdescr.data)
        try:
            # add role to the database
            db.session.add(list)
            db.session.commit()
            flash('You have successfully added a new list.')
            return redirect(url_for('admin.list_lists'))
        except:
            # in case list already exists
            flash('Error: list name already exists.')
            #redirect to lists page
            return redirect(url_for('admin.list_lists'))
                                                                                                                                                            
    return render_template('admin/lists/list.html', add_list=add_list, 
    				form=form, title='Add List')

@admin.route('/lists/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lists(id):
    """
    Handle requests to edit list contents 
    """
    check_admin()
    add_list=False
    list = ListIndex.query.get_or_404(id)
    form = ListsForm(obj=list)
    if form.validate_on_submit():
        list.listindex=form.listindex.data
        list.itemindex=form.itemindex.data
        list.itemname=form.itemname.data
        list.itemdescr=form.itemdescr.data
        # add list item to the database
        db.session.add(list)
        db.session.commit()
        flash('Your edits have been comitted.')

        # redirect to the list page
        return redirect(url_for('admin.list_lists'))

    form.listindex.data=list.id
    form.itemindex=list.itemid
    form.itemname=list.itemname
    form.itemdescr.data= list.descr
    return render_template('admin/lists/list.html', add_list=add_list, 
    				form=form, list=list, title='Edit List')

@admin.route('/lists/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_list(id):
    """
    Delete a list from the database
    """
    check_admin()
    list = ListIndex.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    flash('You have successfully deleted the list.')

    # redirect to the lists page
    return redirect(url_for('admin.list_lists'))

    # return render_template(title="Delete List")
    
@admin.route('/lists/list_items/<int:id>', methods=['GET', 'POST'])
@login_required
def list_items(id):
    """
    Show all of the items in a list
    """
	
    check_admin()
    form = ListItemsForm(obj=list)
    if form.validate_on_submit():
        return redirect('admin/lists/edit_list_items', id=id)
    
    q = 'select * from listitems where listindex_id = ' + str(id)
    listitems = db.session.execute(q)
    add_list_item=True
    form.listindex.data=id
    listname=request.args.get("listname")
    return render_template('admin/lists/items.html', add_list_item=add_list_item, 
                    listitems=listitems, listname=listname, id=id, title="List Items")
    

@admin.route('/lists/edit_list_items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_list_items(id):
    """
    Handle requests to edit list items 
    """
    check_admin()
    add_list_item=False
    listitems = ListItems.query.get_or_404(id)
    form = ListsItemsForm(obj=listitems)
    if form.validate_on_submit():
        listitems.listid=form.listid.data
        listitems.itemnameid=form.itemnameid.data
        listitems.itemname=form.itemname.data
        listitems.descr=form.descr.data
        # add list item to the database
        db.session.add(list)
        db.session.commit()
        flash('Your edits have been comitted.')
        # redirect to the list page
        return redirect(url_for('admin.add_list'))
    form.listid.data=listitems.id
    form.itemnameid=listitems.itemnameid
    form.itemname=listitems.itemname
    form.descr.data= listitems.descr
    return render_template('admin/lists/list.html', add_list=add_list, form=form, 
    				listitems=listitems, title='Edit List')

@admin.route('/lists/add_list_item/<int:id>', methods=['GET', 'POST'])
@login_required
def add_list_item(id):
    """
    Add and item to an existing list
    """
    check_admin()
    add_item = True
    form = ListItemsForm()
    if form.validate_on_submit():
        listname = db.session.execute('select listname from listindex where listid=' + str(id))
        listname = listname.first()
        listitem = ListItems(listindex_id=form.listindex.data, itemname=form.itemname.data, 
        			itemdescr=form.itemdescr.data, itemindex=form.itemindex.data)

        try:
            db.session.add(listitem)
            db.session.commit()
            flash('Item successfully added to the list')
            q = 'select * from listitems where listindex_id = ' + str(id)
            listitems = db.session.execute(q)
            add_list_item=False
            return render_template('admin/lists/items.html', add_list_item=add_list_item,
                                        listname=listname, listitems=listitems, id=id, title="List Items")
        except:
            flash('Unable to add list item')
            return redirect(url_for('admin.list_items', id=id, listname=listname))
    q = 'select listname from listindex where listindex.id = ' + str(id)
    listqry = db.session.execute(q)
    listname=request.args.get("listname")
    form.listindex.data=id
    form.listname.data=listname
    return render_template('admin/lists/list.html', add_item=add_item, listqry=listqry,  
    				form=form, id=id, listname=listname, title='Add List Item')

@admin.route('/lists/delete_list_item/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_list_item(id):
    """
    Delete a list_item from the database
    """
    check_admin()
    listitem = ListItems.query.get_or_404(id)
    listid = listitem.listindex
    db.session.delete(listitem)
    db.session.commit()
    flash('You have successfully deleted the list item.')

    # redirect to the departments page
    # return redirect(url_for('admin.edit_list_items', id=id))

    return redirect(url_for('admin.list_items', id=id))                                     

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')



