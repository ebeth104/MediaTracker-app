from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app import app
from app.api_calls import get_movie_details, get_tv_show_details
from app.auth import db
from app.auth.models import User
from app.account.models import Review, WatchedItem, WatchlistItem

    
@app.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username
    return render_template('account/dashboard.html', username=username)


@app.route('/add_to_watchlist/<string:item_type>/<int:item_id>')
@login_required
def add_to_watchlist(item_type, item_id):
    
    user_id = current_user.id

    if current_user.is_authenticated:

        # Choose the appropriate function based on item type
        if item_type == 'movie':
            item_details = get_movie_details(item_id)
        elif item_type == 'tv':
            item_details = get_tv_show_details(item_id)
        else:
            flash('Invalid item type.', 'danger')
            return redirect(url_for('index'))

    # Create a new WatchlistItem
    watchlist_item = WatchlistItem(
        user_id=user_id,
        item_id=item_id,
        title=item_details.get('title') or item_details.get('original_name')
                or item_details.get('original_title')
                or item_details.get('name'),
        poster=item_details['poster_path'])
    
    # Add and commit to the database
    db.session.add(watchlist_item)
    db.session.commit()
    
    flash('Item added to watchlist successfully.', 'success')
    return redirect(url_for('watchlist'))

@app.route('/remove_from_watchlist/<int:item_id>')
@login_required
def remove_from_watchlist(item_id):
    user_id = current_user.id

    # Query the WatchlistItem and delete it
    watchlist_item = WatchlistItem.query.filter_by(user_id=user_id, item_id=item_id).first()

    if watchlist_item:
        db.session.delete(watchlist_item)
        db.session.commit()
        flash('Item removed from watchlist.', 'success')
    else:
        flash('Item not found in watchlist.', 'danger')

    return redirect(url_for('watchlist'))

@app.route('/watchlist')
@login_required
def watchlist():
    
    user_id = current_user.id

    # Retrieve watchlist items for the current user
    watchlist_items = WatchlistItem.query.filter_by(user_id=user_id).all()

    return render_template('account/watchlist.html', watchlist_items=watchlist_items)


@app.route('/add_to_watched/<string:item_type>/<int:item_id>')
@login_required
def add_to_watched(item_type, item_id):
    
    user_id = current_user.id

    if current_user.is_authenticated:

        # Choose the appropriate function based on item type
        if item_type == 'movie':
            item_details = get_movie_details(item_id)
        elif item_type == 'tv':
            item_details = get_tv_show_details(item_id)
        elif item_type == 'watchlist':
            watchlist_item = WatchlistItem.query.filter_by(user_id=user_id, item_id=item_id).first()
            
            if watchlist_item:
                item_details = {
                    'title': watchlist_item.title,
                    'poster_path': watchlist_item.poster,
                    'user_id' : watchlist_item.user_id,
                    'item_id' : watchlist_item.item_id
                }
            else:
                flash('Item not found in watchlist.', 'danger')
                return redirect(url_for('index'))
        else:
            flash('Invalid item type.', 'danger')
            return redirect(url_for('index'))

    # Create a new WatchedItem
    watched_item = WatchedItem(
        title=item_details.get('title') or item_details.get('original_name') 
                or item_details.get('original_title') 
                or item_details.get('name') or 'Unknown Title',
        user_id=user_id,
        item_id=item_id,
        poster=item_details['poster_path']
    )

    # Add and commit to the database
    db.session.add(watched_item)
    db.session.commit()

    flash('Item added to Watched successfully.', 'success')
    return redirect(url_for('watched'))

@app.route('/remove_from_watched/<int:item_id>')
@login_required
def remove_from_watched(item_id):
    user_id = current_user.id

    # Query the WatchedItem and delete it
    watched_item = WatchedItem.query.filter_by(user_id=user_id, item_id=item_id).first()

    if watched_item:
        db.session.delete(watched_item)
        db.session.commit()
        flash('Item removed from watched list.', 'success')
    else:
        flash('Item not found in watched list.', 'danger')

    return redirect(url_for('watched'))

@app.route('/watched')
def watched():
    user_id = current_user.id

    # Retrieve watched items for the current user
    watched_items = WatchedItem.query.filter_by(user_id=user_id).all()

    return render_template('account/watched.html', watched_items=watched_items)

@app.route('/review/<int:item_id>')
@login_required
def review(item_id):
    
    watched_item = WatchedItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    item_details = {
                        'title': watched_item.title,
                        'user_id' : watched_item.user_id,
                        'item_id' : watched_item.item_id,
                        'poster_path': watched_item.poster
                    }
    return render_template('account/reviewpage.html',item_details=item_details )

@app.route('/user_reviews')
@login_required
def user_reviews():
    user_id = current_user.id
    user_reviews = Review.query.filter_by(user_id=user_id).all()
    return render_template('account/user_reviews.html', user_reviews=user_reviews)

@app.route('/add_review/<string:item_type>/<int:item_id>', methods=['GET','POST'])
@login_required
def add_review(item_type, item_id):
    user_id = current_user.id

    if current_user.is_authenticated:
        if item_type == 'movie':
            item_details = get_movie_details(item_id)
        elif item_type == 'tv':
            item_details = get_tv_show_details(item_id)
        elif item_type == 'watched':
            watched_item = WatchedItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()

            if watched_item:
                    item_details = {
                        'title': watched_item.title,
                        'user_id' : watched_item.user_id,
                        'item_id' : watched_item.item_id,
                        'poster_path': watched_item.poster
                    }
            else:
                flash('Item not found in watched list.', 'danger')
                return redirect(url_for('index'))
        else:
            flash('Invalid item type.', 'danger')
            return redirect(url_for('index'))
    
    # Create a new ReviewItem
    if request.method == 'POST':
        review = Review(
            title=item_details.get('title') or item_details.get('original_name') 
                    or item_details.get('original_title') 
                    or item_details.get('name') or 'Unknown Title',
            user_id=user_id,
            item_id=item_details['item_id'],
            poster=item_details['poster_path'],
            reviews=request.form.get('review'),
            notes=request.form.get('notes'))

    # Add and commit to the database
    db.session.add(review)
    db.session.commit()

    flash('Added successfully.', 'success')
    return redirect(url_for('review', item_id=item_id))

@app.route('/update_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)

    if request.method == 'POST':
        # Update the review with the new data
        review.reviews = request.form.get('reviews')
        review.notes = request.form.get('notes')

        # Commit changes to the database
        db.session.commit()

        flash('Review updated successfully.', 'success')
        return redirect(url_for('user_reviews'))

    return render_template('account/update_review.html', review=review)

@app.route('/profile')
def profile():
    user_id=current_user.id 
    
    user_details = User.query.filter_by(id=user_id).first()
    
    return render_template('account/profile.html', user_details=user_details)





