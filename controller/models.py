from controller.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    user_Role = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), nullable=False) 
    is_approved = db.Column(db.Boolean, default=False)

    #Relationship
    student_profile = db.relationship('StudentProfile', backref='user', lazy=True, uselist=False)
    company_profile = db.relationship('CompanyProfile', backref='user', lazy=True, uselist=False)
    roles = db.relationship('Role', secondary='user_role', back_populates='users', viewonly=True, lazy=True)
    blacklist = db.relationship('Blacklist', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f'<User {self.user_email}>'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    #Relationship
    users = db.relationship('User', secondary='user_role', back_populates='roles', viewonly=True, lazy=True)

    def __repr__(self):
        return f'<Role {self.name}>' 


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    #relationship
    user = db.relationship('User', backref=db.backref('user_roles', overlaps="roles, users"), lazy=True)
    role = db.relationship('Role', backref=db.backref('user_roles', overlaps="roles, users"), lazy=True)

class CompanyProfile(db.Model):
    __tablename__ = 'company_profile'
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    company_mail = db.Column(db.String(120), nullable=False)
    Hr_contact = db.Column(db.String(10), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    company_description = db.Column(db.Text, nullable=True)

    placement_drives = db.relationship('PlacementDrive', backref='company', lazy=True)

    def __repr__(self):
        return f'<CompanyProfile {self.company_name}>'
    
class StudentProfile(db.Model):
    __tablename__ = 'student_profile'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    student_mail = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    city_state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(256), nullable=False)
    university = db.Column(db.String(120), nullable=True)
    course = db.Column(db.String(50), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    location_preference = db.Column(db.String(120), nullable=True)
    work_mode_preference = db.Column(db.String(20), nullable=True)
    job_preference = db.Column(db.String(120), nullable=True) # Internship, Full-time, Part-time, Freelance
    experience = db.Column(db.Text, nullable=True)
    resume = db.Column(db.String(256))
    linkedin_profile = db.Column(db.String(256), nullable=True)
    github_profile = db.Column(db.String(256), nullable=True)

    applications = db.relationship('Application', backref='student', lazy=True)

    def __repr__(self):
        return f'<StudentProfile {self.first_name} {self.last_name}>'  

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    placement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.company_id'), nullable=False)
    job_role = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    job_mode = db.Column(db.String(20), nullable=False)
    job_type = db.Column(db.String(20), nullable=False) # On-campus or Off-campus
    job_location = db.Column(db.String(120), nullable=True)
    work_hours = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.Float, nullable=True)
    eligibility_criteria = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(256), nullable=True)
    deadline = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Open or Closed
    is_approved = db.Column(db.Boolean, default=False)

    applications = db.relationship('Application', backref='placement_drive', lazy=True)

    def __repr__(self):
        return f'<PlacementDrive {self.job_role} at Company ID {self.company_id}>'  
    
class Application(db.Model):
    __tablename__ = 'application'
    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.student_id'), nullable=False)
    placement_id = db.Column(db.Integer, db.ForeignKey('placement_drive.placement_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False) # Applied, Shortlisted, Rejected, Accepted
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Application Student ID {self.student_id} for Placement ID {self.placement_id}>'
    
class Blacklist (db.Model):
    __tablename__ = 'blacklist'
    blacklist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    def __repr__(self):
        return f'<Blacklist User ID {self.user_id}>' 




