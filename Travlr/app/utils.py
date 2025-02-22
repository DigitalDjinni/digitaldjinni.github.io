from flask import redirect, url_for, flash
from flask_login import current_user

# Checks if the user is an admin before allowing access to certain routes
def check_admin():
    if not current_user.is_admin:
        flash('You don’t have admin access.', 'danger')
        return redirect(url_for('trip_blueprint.list_trips'))
    return None  # Returns nothing if the user is an admin
