from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Trip
from app.forms import AddTripForm, EditTripForm, TripSearchForm 
from app import db
from app.utils import check_admin
import logging

# Creates a Blueprint for the trip routes
trip_blueprint = Blueprint('trip_blueprint', __name__)

# Index Page Route
@trip_blueprint.route('/', methods=['GET'])
def home():
    return render_template('index.html', is_logged_in=current_user.is_authenticated)

# Rooms Page Route
@trip_blueprint.route('/rooms', methods=['GET'])
def rooms():
    return render_template('rooms.html', is_logged_in=current_user.is_authenticated)

# News Page Route
@trip_blueprint.route('/news', methods=['GET'])
def news():
    return render_template('news.html', is_logged_in=current_user.is_authenticated)

# Contact Page Route
@trip_blueprint.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', is_logged_in=current_user.is_authenticated)

# Meals Page Route
@trip_blueprint.route('/meals', methods=['GET'])
def meals():
    return render_template('meals.html', is_logged_in=current_user.is_authenticated)

# About Page Route
@trip_blueprint.route('/about', methods=['GET'])
def about():
    return render_template('about.html', is_logged_in=current_user.is_authenticated)

# Trips Page Route 
@trip_blueprint.route('/trips', methods=['GET', 'POST'])
def list_trips():
    try:
        form = TripSearchForm(request.args)  # Makes sure request.args is used to fill form

        # Start with all trips from database
        trips_query = Trip.query

        # Apply search filters if the parameters exist
        if request.args.get('query'):
            trips_query = trips_query.filter(Trip.name.ilike(f"%{request.args.get('query')}%"))
        if request.args.get('min_price'):
            trips_query = trips_query.filter(Trip.per_person >= float(request.args.get('min_price')))
        if request.args.get('max_price'):
            trips_query = trips_query.filter(Trip.per_person <= float(request.args.get('max_price')))
        if request.args.get('start_date'):
            trips_query = trips_query.filter(Trip.start >= request.args.get('start_date'))

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = 9
        pagination = trips_query.paginate(page=page, per_page=per_page, error_out=False)
        trips = pagination.items

        return render_template('trips.html', trips=trips, pagination=pagination, form=form, is_logged_in=current_user.is_authenticated)

    except Exception as e:
        logging.error(f"Error in list_trips: {e}")
        flash('An error occurred while trying to fetch trips. Please try again later.', 'danger')
        return render_template('error.html', error_message="Unable to fetch trips from database.")

# Route to view specific trip
@trip_blueprint.route('/trips/<int:trip_id>', methods=['GET'])
def view_trip(trip_id):
    try:
        trip = Trip.query.get_or_404(trip_id)  
        return render_template('view_trip.html', trip=trip)
    except Exception as e:
        logging.error(f"Error occured while trying to fetch trip {trip_id}: {e}")
        flash('Unable to fetch trip details.', 'danger')
        return render_template('error.html', error_message="Unable to fetch trip details.")

# Search Route
@trip_blueprint.route('/trips/search', methods=['POST'])
def search_trips():
    form = TripSearchForm()

    if form.validate_on_submit():
        # print(f"Search Data Received: {form.query.data}, {form.min_price.data}, {form.max_price.data}, {form.start_date.data}")

        return redirect(url_for('trip_blueprint.list_trips',
                                query=form.query.data or "",
                                min_price=form.min_price.data or "",
                                max_price=form.max_price.data or "",
                                start_date=form.start_date.data or ""))
    flash('Invalid Search Entry.', 'danger')
    return redirect(url_for('trip_blueprint.list_trips'))  


# Add Trip Route (Admin only)
@trip_blueprint.route('/trips/add', methods=['GET', 'POST'])
@login_required
def add_trip():
    admin_redirect = check_admin()
    if admin_redirect:
        return admin_redirect 

    form = AddTripForm()
    if form.validate_on_submit():
        try:
            new_trip = Trip(
                code=form.code.data,
                name=form.name.data,
                length=form.length.data,
                start=form.start.data,
                resort=form.resort.data,
                per_person=form.per_person.data,
                image=form.image.data,
                description=form.description.data,
            )
            db.session.add(new_trip)
            db.session.commit()
            flash('Trip was added successfully!', 'success')
            return redirect(url_for('trip_blueprint.list_trips'))
        except Exception as e:
            logging.error(f"Error adding trip: {e}")
            db.session.rollback()
            flash('An error occurred while adding the trip. Please try again.', 'danger')

    return render_template('add_trip.html', form=form)

# Edit Trip Route (Admin only)
@trip_blueprint.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    admin_redirect = check_admin()
    if admin_redirect:
        return admin_redirect 

    trip = Trip.query.get_or_404(trip_id)
    form = EditTripForm(obj=trip)  

    if form.validate_on_submit():
        try:
            trip.code = form.code.data
            trip.name = form.name.data
            trip.length = form.length.data
            trip.start = form.start.data
            trip.resort = form.resort.data
            trip.per_person = form.per_person.data
            trip.image = form.image.data
            trip.description = form.description.data

            db.session.commit()
            flash('Trip was updated successfully!', 'success')
            return redirect(url_for('trip_blueprint.list_trips'))
        except Exception as e:
            logging.error(f"Error editing trip {trip_id}: {e}")
            db.session.rollback()
            flash('An error occurred while updating the trip. Please try again.', 'danger')

    return render_template('edit_trip.html', form=form, trip=trip)

# Delete Trip Route (Admin only)
@trip_blueprint.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    admin_redirect = check_admin()
    if admin_redirect:
        return admin_redirect

    trip = Trip.query.get_or_404(trip_id)

    try:
        db.session.delete(trip)
        db.session.commit()
        flash('Trip was deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"There was an error deleting trip {trip_id}: {e}")
        db.session.rollback()
        flash('An error occurred while deleting the trip. Please try again.', 'danger')

    return redirect(url_for('trip_blueprint.list_trips'))
