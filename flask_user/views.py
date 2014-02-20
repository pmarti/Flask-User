from flask import current_app, flash, redirect, render_template, request, url_for
import flask_login


def register():
    um = current_app.user_manager

    # Initialize form
    form = um.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        hashed_password = um.crypt_context.encrypt(form.password.data)
        if um.login_with_username:
            um.db_adapter.add_user(
                username=form.username.data,
                password=hashed_password)
        else:
            um.db_adapter.add_user(
                email=form.email.data,
                password=hashed_password)
        return redirect(um.login_url)

    # Process GET or invalid POST
    return render_template(um.register_template, user_manager=um, form=form)

def login():
    um = current_app.user_manager

    # Initialize form
    form = um.login_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Retrieve User
        if um.login_with_username:
            user = um.db_adapter.find_user_by_username(form.username.data)
        elif um.login_with_email:
            user = um.db_adapter.find_user_by_email(form.email.data)
        else:
            user = None

        if user:
            # Use Flask-Login to sign in user
            flask_login.login_user(user)

            # Prepare Flash message
            flash(um.flash_signed_in, 'success')

            # Redirect to 'next' URL or '/'
            next = form.next.data
            if not next:
                return redirect('/')
            return redirect(next)

    # Process GET or invalid POST
    return render_template(um.login_template, user_manager=um, form=form)

def logout():
    um = current_app.user_manager

    # Use Flask-Login to sign out user
    flask_login.logout_user()

    # Prepare Flash message
    flash(um.flash_signed_out, 'success')

    # Redirect to logout_next endpoint or '/'
    if um.logout_next:
        return redirect(url_for(um.logout_next))
    else:
        return redirect('/')