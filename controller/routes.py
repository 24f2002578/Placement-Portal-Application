from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controller.models import *
import os


@app.route('/home')
def home():
    if 'user_email' in session:
        user_id = session.get('user_id')
        current_student = StudentProfile.query.filter_by(user_id=user_id).first()
        return render_template('home.html', students=StudentProfile.query.all(), companies=CompanyProfile.query.all(), current_student=current_student)
    return render_template('home.html')
    

# Student Profile Route
@app.route('/studentinfo', methods=['GET', 'POST'])
def studentinfo():
    if request.method == 'GET':
        if 'user_email' in session and 'user_id' in session:
            return render_template('Student_detail.html')
        flash('Please log in to create student profile')
        return redirect('/login')

    # POST
    user_id = session.get('user_id')
    if not user_id:
        flash('Session expired, please log in again')
        return redirect('/login')
    
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
    return render_template('student_dashboard.html')

#Company Profile Route
@app.route('/companyinfo', methods=['GET', 'POST'])
def companyinfo():
    if request.method == 'GET':
        if 'user_email' in session and 'user_id' in session:
            return render_template('Company_detail.html')
        flash('Please log in to access company info')
        return redirect('/login')

    # POST
    user_id = session.get('user_id')
    if not user_id:
        flash('Session expired, please log in again')
        return redirect('/login')

    company_name = request.form.get('company_name')
    company_mail = request.form.get('company_mail')
    Hr_contact = request.form.get('Hr_contact') 
    website = request.form.get('website')
    company_description = request.form.get('company_description')


    if not company_name or not company_mail or not Hr_contact:
        flash('Please fill in all required fields')
        return render_template('Company_detail.html')
    new_companyinfo = CompanyProfile(
        user_id=user_id,
        company_name=company_name.strip(),
        company_mail=company_mail.strip(),
        Hr_contact=Hr_contact.strip(),
        website=website.strip(),
        company_description=company_description.strip() if company_description else None
    )
    
    
    db.session.add(new_companyinfo)
    db.session.commit()

    flash('Company information submitted successfully')
    return render_template('company_dashboard.html')

@app.route('/drive', methods=['GET', 'POST'])
def drive():
    if request.method == 'GET':
        if 'company_id' in session and 'user_id' in session:
            return render_template('drive.html')
        flash('Complete your company profile to access placement drive features')
        return redirect('/companyinfo') #Yeahhhhhhhhhh, dinga laka laka

    # POST
    company_id = session.get('company_id')
    if not company_id:
        flash('Session expired, please log in again')
        return redirect('/login')

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
    return render_template('company_dashboard.html')

@app.route('/drives')
def drives():
    return render_template('drive.html')
                           
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

@app.route('/delete_drive/<int:user_id>')
def delete_drive(user_id):
    if 'admin' not in session.get('user_role', [None]):
        flash('you are not authorized to delete drive')
        return redirect('/home')
    drive = PlacementDrive.query.filter_by(user_id=user_id).first()
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
