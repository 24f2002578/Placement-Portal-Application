from flask import Flask, render_template
from controller.database import db
from controller.config import Config
from controller.models import *

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

    #Clarifying Roles

    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        
    student_role = Role.query.filter_by(name='student').first()
    if not student_role:
        student_role = Role(name='student')
        db.session.add(student_role)

    company_role = Role.query.filter_by(name='company').first()
    if not company_role:    
        company_role = Role(name='company')
        db.session.add(company_role)

    #Creating an admin user if not exists

    admin_user = User.query.filter_by(user_email='24f2002578@ds.study.iitm.ac.in').first()
    if not admin_user:
        admin_user = User(user_email='24f2002578@ds.study.iitm.ac.in',password='Admin123',user_name='Modi', is_approved=True)
        db.session.add(admin_user)
        #print(admin_user.id)
        admin_user_details = User.query.filter_by(user_email = '24f2002578@ds.study.iitm.ac.in').first()
        admin_role = Role.query.filter_by(name='admin').first()
        user_id = admin_user.user_id
        role_id = admin_role.id 

        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.session.add(user_role)


    db.session.commit()

from controller.auth_routes import *
from controller.routes import *


if __name__ == '__main__':
    app.run()