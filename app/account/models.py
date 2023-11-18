from app.auth import db 

class WatchlistItem(db.Model):
    __tablename__ = 'watchlist_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f'WatchlistItem(id={self.id}, title={self.title})'
    
class WatchedItem(db.Model):
    __tablename__ = 'watched_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f'WatchedItem(id={self.id}, title={self.title})'
    
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(128), nullable=False)
    reviews = db.Column(db.TEXT(1000), nullable=False)
    notes = db.Column(db.TEXT(1000), nullable=False)
    
    def __repr__(self):
        return f'WatchedItem(id={self.id}, title={self.title})'
