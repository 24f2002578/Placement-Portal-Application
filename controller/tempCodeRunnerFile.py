 if request.method == 'POST':
        fullname = request.form.get('fullname', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        role = request.form.get('role', None)
        password = request.form.get('password', None)
        confirm_password = request.form.get('confirm-password', None)