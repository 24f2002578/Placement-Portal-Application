from main import app, db
from controller.models import User

def approve_all_students():
    with app.app_context():
        # Find all students who are currently unapproved
        students_to_approve = User.query.filter_by(user_Role='student', is_approved=False).all()
        
        count = 0
        for student in students_to_approve:
            student.is_approved = True
            count += 1
            
        db.session.commit()
        print(f"Successfully auto-approved {count} existing students.")

if __name__ == "__main__":
    approve_all_students()
