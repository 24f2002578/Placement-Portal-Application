from controller.models import PlacementDrive
from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controller.models import *
import os


@app.route('/home')
def home():
    if 'user_email' in session:
        user_id = session.get('user_id')
        current_student = StudentProfile.query.filter_by(user_id=user_id).first()
        current_company = CompanyProfile.query.filter_by(user_id=user_id).first()
        drives = []
        if current_company:
            drives = PlacementDrive.query.filter_by(company_id=current_company.company_id).all()
        approved_students = [s for s in StudentProfile.query.all() if s.user and s.user.is_approved and not s.user.blacklist]
        approved_companies = [c for c in CompanyProfile.query.all() if c.user and c.user.is_approved and not c.user.blacklist]
        open_drives = PlacementDrive.query.filter_by(status='Open').all()
        return render_template('home.html', students=approved_students, companies=approved_companies, current_student=current_student, current_company=current_company, drives=drives, open_drives=open_drives)
    return render_template('home.html')
    

# Student Profile Route
@app.route('/studentinfo', methods=['GET', 'POST'])
def studentinfo():
    if 'user_email' not in session or 'user_id' not in session:
        flash('Please log in to create student profile')
        return redirect('/login')

    user_id = session.get('user_id')

    existing_profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        flash('Profile already created! You have been redirected to edit your profile.')
        return redirect(url_for('edit_student', user_id=user_id))

    if request.method == 'GET':
        return render_template('Student_detail.html')
    
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        student_mail = request.form.get('student_mail')
        contact = request.form.get('contact')
        age = request.form.get('age')
        gender = request.form.get('gender')
        qualification = request.form.get('qualification')
        college = request.form.get('college')
        university = request.form.get('university')
        course = request.form.get('course')
        graduation_year = request.form.get('graduation_year')
        address = request.form.get('address')
        city_state = request.form.get('city_state')
        job_preference = request.form.get('job_preference')
        work_mode_preference = request.form.get('work_mode_preference')
        location_preference = request.form.get('location_preference')
        experience = request.form.get('experience')
        Resume = request.files.get('resume', None)
        linkedin_profile = request.form.get('linkedin_profile')
        github_profile = request.form.get('github_profile')
        resume= None

        if Resume:
            folder=os.path.join(app.config['UPLOAD_FOLDER'], 'student_resume')
            filename=Resume.filename
            Resume.save(os.path.join(folder,filename))
            resume=os.path.join('student_resume/',filename) 


    if not firstname or not lastname or not student_mail or not contact or not age or not gender or not qualification or not college or not course or not graduation_year or not address or not city_state or not resume:
        flash('Please fill in all required fields')
        return render_template('Student_detail.html')

            
    new_studentinfo = StudentProfile(
         user_id=user_id,
        first_name=firstname.strip(),
        last_name=lastname.strip(),
        student_mail=student_mail.strip(),
        contact=contact.strip(),
        age=age.strip(),
        gender=gender.strip(),
        qualification=qualification.strip(),
        college=college.strip(),
        university=university.strip() if university else None,
        course=course.strip(),
        graduation_year=graduation_year.strip(),
        address=address.strip(),
        city_state=city_state.strip(),
        job_preference=job_preference.strip() if job_preference else None,
        work_mode_preference=work_mode_preference.strip() if work_mode_preference else None,
        location_preference=location_preference.strip() if location_preference else None,
        experience=experience.strip() if experience else None,
        resume=resume if resume else None,
        linkedin_profile=linkedin_profile.strip() if linkedin_profile else None,
        github_profile=github_profile.strip() if github_profile else None
    )
    db.session.add(new_studentinfo)
    db.session.commit()
        
    flash('Student information submitted successfully')
    return redirect(url_for('home'))

#Company Profile Route
@app.route('/companyinfo', methods=['GET', 'POST'])
def companyinfo():
    if request.method == 'GET':
        if 'user_email' in session and 'user_id' in session:
            return render_template('company_detail.html')
        
        flash('Please log in to access company info')
        return redirect('/login')

    # POST
    user_id = session.get('user_id')
    if 'company' not in session.get('user_role', [None]):
        flash('You Don\'t Have A Company Profile')
        return redirect('/home')

    company_name = request.form.get('company_name')
    company_mail = request.form.get('company_mail')
    Hr_contact = request.form.get('Hr_contact') 
    website = request.form.get('website')
    company_description = request.form.get('company_description')


    if not company_name or not company_mail or not Hr_contact:
        flash('Please fill in all required fields')
        return render_template('company_detail.html')
    new_companyinfo = CompanyProfile(
        user_id=user_id,
        company_name=company_name.strip(),
        company_mail=company_mail.strip(),
        Hr_contact=Hr_contact.strip(),
        website=website.strip() if website else None,
        company_description=company_description.strip() if company_description else None
    )
    
    
    db.session.add(new_companyinfo)
    db.session.commit()

    flash('Company information submitted successfully')
    return redirect(url_for('home'))

@app.route('/drive', methods=['GET', 'POST'])
def drive():
    user_id = session.get('user_id')
    if not user_id:
        flash('Session expired, please log in again')
        return redirect(url_for('login'))
        
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if request.method == 'GET':
        if company:
            return render_template('drive.html')
        flash('Complete your company profile to access placement drive features')
        return redirect(url_for('companyinfo'))

    # POST
    if not company:
        flash('Complete your company profile first')
        return redirect(url_for('companyinfo'))
        
    company_id = company.company_id

    job_role = request.form.get('job_role')
    job_description = request.form.get('job_description')
    job_type = request.form.get('job_type')
    job_mode = request.form.get('job_mode')
    job_location = request.form.get('job_location')
    work_hours = request.form.get('work_hours')
    salary = request.form.get('salary')
    deadline = request.form.get('deadline')
    eligibility_criteria = request.form.get('eligibility_criteria')
    skills = request.form.get('skills')
    status = request.form.get('status')


    if not job_role or not job_description:
        flash('Please fill in all required fields')
        return render_template('drive.html')
    new_placement_drive = PlacementDrive(
        company_id=company_id,
        job_role=job_role.strip(),
        job_description=job_description.strip(),
        job_type=job_type.strip(),
        job_mode=job_mode.strip(),
        job_location=job_location.strip(),
        work_hours=work_hours.strip(),
        salary=salary.strip(),
        deadline=deadline.strip(),
        eligibility_criteria=eligibility_criteria.strip() if eligibility_criteria else None,
        skills=skills.strip() if skills else None,
        status=status.strip()
    )   

    db.session.add(new_placement_drive)
    db.session.commit()

    flash('Placement drive created successfully')
    return redirect(url_for('home'))


@app.route('/delete_student/<int:user_id>')
def delete_student(user_id):
    if 'user_email' not in session:
        flash('you are not authorized to delete student')
        return redirect('/home')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    db.session.delete(student)
    db.session.commit()
    flash('Student Profile deleted successfully')
    return redirect(url_for('home'))

@app.route('/delete_company/<int:user_id>')
def delete_company(user_id):
    if 'company' not in session.get('user_role', [None]):
        flash('you are not authorized to delete company')
        return redirect('/home')
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        flash('Company not found')
        return redirect(url_for('home'))
    db.session.delete(company)
    db.session.commit()
    flash('Company Profile deleted successfully')
    return redirect(url_for('home'))

@app.route('/delete_drive/<int:placement_id>')
def delete_drive(placement_id):
    if 'user_id' not in session:
        flash('you are not authorized to delete drive')
        return redirect('/home')
    drive = PlacementDrive.query.filter_by(placement_id=placement_id).first()
    if not drive:
        flash('Drive not found')
        return redirect(url_for('home'))
    db.session.delete(drive)
    db.session.commit()
    flash('Placement Drive deleted successfully')
    return redirect(url_for('home'))

@app.route('/edit_company/<int:user_id>', methods=['GET', 'POST'])
def edit_company(user_id):
    if 'company' not in session.get('user_role', [None]):
        flash('You Don\'t Have A Company Profile')
        return redirect('/home')
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        flash('Company not found')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('edit_company.html', company=company)
    
    # POST
    company_name = request.form.get('company_name')
    company_mail = request.form.get('company_mail')
    Hr_contact = request.form.get('Hr_contact') 
    website = request.form.get('website')
    company_description = request.form.get('company_description')

    company.company_name = company_name.strip()
    company.company_mail = company_mail.strip()
    company.Hr_contact = Hr_contact.strip()
    company.website = website.strip() if website else None
    company.company_description = company_description.strip() if company_description else None

    db.session.commit()
    flash('Company Profile updated successfully')
    return redirect(url_for('home'))

@app.route('/edit_student/<int:user_id>', methods=['GET', 'POST'])
def edit_student(user_id):
    if 'student' not in session.get('user_role', [None]):
        flash('You Don\'t Have A Student Profile')
        return redirect('/home')
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    if not student:
        flash('Student not found')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('edit_student.html', user_id=user_id, student=student)

    # POST
    firstname = request.form.get('firstname', None)
    lastname = request.form.get('lastname', None)
    student_mail = User.query.filter_by(user_email=session['user_email']).first().user_email
    contact = request.form.get('contact', None)
    age = request.form.get('age', None)
    qualification = request.form.get('qualification', None)
    college = request.form.get('college', None)
    university = request.form.get('university', None)
    course = request.form.get('course', None)
    graduation_year = request.form.get('graduation_year')
    address = request.form.get('address', None)
    city_state = request.form.get('city_state', None)
    job_preference = request.form.get('job_preference', None)
    work_mode_preference = request.form.get('work_mode_preference', None)
    location_preference = request.form.get('location_preference', None)
    experience = request.form.get('experience', None)
    Resume = request.files.get('resume', None)
    linkedin_profile = request.form.get('linkedin_profile', None)
    github_profile = request.form.get('github_profile', None)

    resume=None

    if Resume:
        folder=os.path.join(app.config['UPLOAD_FOLDER'], 'student_resume')
        filename=Resume.filename
        Resume.save(os.path.join(folder,filename))
        resume=os.path.join('student_resume/',filename)

    student.first_name = firstname
    student.last_name = lastname
    student.age = age
    student.student_mail = student_mail
    student.contact = contact
    student.qualification = qualification
    student.college = college
    student.university = university
    student.course = course
    student.graduation_year = graduation_year
    student.address = address
    student.city_state = city_state
    student.job_preference = job_preference
    student.work_mode_preference = work_mode_preference
    student.location_preference = location_preference
    student.experience = experience
    student.resume = resume
    student.linkedin_profile = linkedin_profile
    student.github_profile = github_profile

    db.session.commit()
    flash('Student Profile updated successfully')
    return redirect(url_for('home'))

@app.route('/edit_drive/<int:placement_id>', methods=['GET', 'POST'])
def edit_drive(placement_id):
    if 'company' not in session.get('user_role', [None]):
        flash('You Don\'t Have A Company Profile')
        return redirect('/home')
    drive = PlacementDrive.query.filter_by(placement_id=placement_id).first()
    if not drive:
        flash('Drive not found, Create a Drive')
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('edit_drive.html', placement_id=placement_id, drive=drive)
    
    # POST
    job_role = request.form.get('job_role')
    job_description = request.form.get('job_description')
    job_type = request.form.get('job_type')
    job_mode = request.form.get('job_mode')
    job_location = request.form.get('job_location')
    work_hours = request.form.get('work_hours')
    salary = request.form.get('salary')
    deadline = request.form.get('deadline')
    eligibility_criteria = request.form.get('eligibility_criteria')
    skills = request.form.get('skills')
    status = request.form.get('status')

    drive.job_role = job_role.strip()
    drive.job_description = job_description.strip()
    drive.job_type = job_type.strip()
    drive.job_mode = job_mode.strip()
    drive.job_location = job_location.strip()
    drive.work_hours = work_hours.strip()
    drive.salary = salary.strip()
    drive.deadline = deadline.strip()
    drive.eligibility_criteria = eligibility_criteria.strip()
    drive.skills = skills.strip()
    drive.status = status.strip()

    db.session.commit()
    flash('Drive updated successfully')
    return redirect(url_for('home'))

@app.route('/blacklist_user/<int:user_id>')
def blacklist_user(user_id):
    if 'admin' not in session.get('user_role', [None]):
        flash('you are not authorized to blacklist user')
        return redirect('/home')
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        flash('User not found')
        return redirect(url_for('home'))
    
    blacklist_entry = Blacklist.query.filter_by(user_id=user.user_id).first()
    if not blacklist_entry:
        db.session.add(Blacklist(user_id=user.user_id))
        
    db.session.commit()
    flash('User blacklisted successfully')
    return redirect(url_for('home'))

@app.route('/remove_blacklist/<int:user_id>')
def remove_blacklist(user_id):
    if 'admin' not in session.get('user_role', [None]):
        flash('you are not authorized to remove blacklist')
        return redirect('/home')
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        flash('User not found')
        return redirect(url_for('home'))
    
    blacklist_entry = Blacklist.query.filter_by(user_id=user.user_id).first()
    if blacklist_entry:
        db.session.delete(blacklist_entry)
        
    db.session.commit()
    flash('User allowlisted successfully')
    return redirect(url_for('home'))

# @app.route('/approve_users', methods=['GET'])
# def approve_users():
#     if 'user_email' in session:
#         return render_template('approve.html',users=User.query.all())
#     flash('you are not authorized to approve user')
#     return redirect('/home')

@app.route('/approve_user/<int:user_id>')
def approve_user(user_id):
    if 'admin' not in session.get('user_role', [None]):
        flash('you are not authorized to approve user')
        return redirect('/home')
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        flash('User not found')
        return redirect(url_for('home'))
    user.is_approved = True
    db.session.commit()
    flash('User approved successfully')
    return redirect(url_for('home'))


@app.route('/reject_user/<int:user_id>')
def reject_user(user_id):
    if 'admin' not in session.get('user_role', []):
        flash('You are not authorized to reject user')
        return redirect('/home')
        
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        flash('User not found')
        return redirect(url_for('home'))
        
    student = StudentProfile.query.filter_by(user_id=user.user_id).first()
    if student:
        db.session.delete(student)
        
    company = CompanyProfile.query.filter_by(user_id=user.user_id).first()
    if company:
        db.session.delete(company)
        
    # Delete roles mapping
    user_roles = UserRole.query.filter_by(user_id=user.user_id).all()
    for ur in user_roles:
        db.session.delete(ur)
        
    blacklist_entry = Blacklist.query.filter_by(user_id=user.user_id).first()
    if blacklist_entry:
        db.session.delete(blacklist_entry)
        
    db.session.delete(user)
    db.session.commit()
    
    flash('User registration rejected and removed')
    return redirect(url_for('approvals'))

@app.route('/approvals')
def approvals():
    if 'admin' not in session.get('user_role', []):
        flash('You are not authorized')
        return redirect('/home')

    keyword = request.args.get('keyword', '').strip().lower()

    unapproved_users = User.query.filter_by(is_approved=False).all()
    blacklisted_users = User.query.join(Blacklist).all()

    if keyword:
        unapproved_users = [u for u in unapproved_users if keyword in (u.user_name or '').lower() or keyword in (u.user_email or '').lower()]
        blacklisted_users = [u for u in blacklisted_users if keyword in (u.user_name or '').lower() or keyword in (u.user_email or '').lower()]

    return render_template('approve.html',
                           unapproved_users=unapproved_users,
                           blacklisted_users=blacklisted_users,
                           keyword=keyword)

from datetime import datetime

@app.route('/apply/<int:placement_id>', methods=['GET', 'POST'])
def apply_drive(placement_id):
    if 'student' not in session.get('user_role', []):
        flash('You must be a student to apply.')
        return redirect(url_for('home'))
        
    student = StudentProfile.query.filter_by(user_id=session.get('user_id')).first()
    if not student:
        flash('Please complete your student profile first before applying.')
        return redirect(url_for('studentinfo'))
        
    drive = PlacementDrive.query.get(placement_id)
    
    # Check if student already applied
    existing_application = Application.query.filter_by(student_id=student.student_id, placement_id=placement_id).first()
    if existing_application:
        flash('You have already applied to this drive.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_app = Application(
            student_id=student.student_id,
            placement_id=placement_id,
            status='Applied'
        )
        db.session.add(new_app)
        db.session.commit()
        
        flash('Application Submitted. Please wait for further updates.')
        return redirect(url_for('home'))
        
    return render_template('student_application.html', drive=drive, student=student)

@app.route('/drive/<int:placement_id>/applications')
def drive_applications(placement_id):
    if 'company' not in session.get('user_role', []):
        flash('Unauthorized access.')
        return redirect(url_for('home'))
        
    company = CompanyProfile.query.filter_by(user_id=session.get('user_id')).first()
    drive = PlacementDrive.query.get(placement_id)
    
    if drive.company_id != company.company_id:
        flash('Unauthorized access.')
        return redirect(url_for('home'))
        
    applications = Application.query.filter_by(placement_id=placement_id).all()
    return render_template('drive_applications.html', drive=drive, applications=applications)

@app.route('/student_profile/<int:student_id>')
def view_student_profile(student_id):
    student = StudentProfile.query.get(student_id)
    if 'user_id' in session:
        return render_template('view_student.html', student=student)
    else:
        return redirect(url_for('home'))
        
    

@app.route('/company_profile/<int:company_id>')
def view_company_profile(company_id):
    company = CompanyProfile.query.get(company_id)
    return render_template('view_company.html', company=company)
    if 'user_id' in session:
        return render_template('view_company.html', company=company)
    else:
        return redirect(url_for('home'))


@app.route('/drive_details/<int:placement_id>')
def view_drive_details(placement_id):
    if 'user_id' in session:
        drive = PlacementDrive.query.get(placement_id)
        return render_template('view_drive.html', drive=drive)
    else:
        return redirect(url_for('home'))

@app.route('/search')
def search(): 
    keyword = request.args.get('keyword', '').strip() # f repredents string jisme variable (keyword here) aa raha hai from html form and query will proceed with keyword
    students = StudentProfile.query.filter(StudentProfile.first_name.ilike(f'%{keyword}%') | StudentProfile.last_name.ilike(f'%{keyword}%')).all()
    companies = CompanyProfile.query.filter(CompanyProfile.company_name.ilike(f'%{keyword}%')).all()
    placements = PlacementDrive.query.filter(PlacementDrive.job_role.ilike(f'%{keyword}%')).all() 
    return render_template('search.html', keyword=keyword, students=students, companies=companies, placements=placements)

@app.route('/select_app/<int:application_id>')
def select_app(application_id):
    if 'company' not in session.get('user_role', []):
        flash('Unauthorized access.')
        return redirect(url_for('home'))
    application = Application.query.get(application_id)
    application.status = 'Selected'
    db.session.commit()
    return redirect(url_for('drive_applications', placement_id=application.placement_id))

@app.route('/reject_app/<int:application_id>')
def reject_app(application_id):
    if 'company' not in session.get('user_role', []):
        flash('Unauthorized access.')
        return redirect(url_for('home'))
    application = Application.query.get(application_id)
    application.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('drive_applications', placement_id=application.placement_id))

