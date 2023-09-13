from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True,
                         autoincrement = True)
    full_name = db.Column( db.String(100),nullable = False)
    user_name = db.Column(db.String(), nullable = False, unique = True)
    email = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    last_login = db.Column(db.String(), nullable = True)
    admin = db.Column(db.Boolean, default= False)
    booking = db.relationship('Bookings', backref = 'user_',
                              cascade = 'all, delete')

class Movies(db.Model):
    movie_id = db.Column(db.Integer(), primary_key = True, 
                         autoincrement = True)
    movie_name = db.Column(db.String(), nullable = False) 
    rating = db.Column(db.Float, nullable = True)
    rating_count = db.Column(db.Float, nullable = True)
    tags = db.Column(db.String, nullable = True)
    language = db.Column(db.String, nullable = True)
    picture = db.Column(db.LargeBinary(), nullable = True)
    show = db.relationship('Shows', backref='movie_1',
                           cascade = 'all, delete', 
                           primaryjoin = 'Shows.movie==Movies.movie_id')
    booking = db.relationship('Bookings', backref = 'movie_2',
                              cascade = 'all, delete',
                              primaryjoin = 'Bookings.movie ==Movies.movie_id')
    pass

class  Venues(db.Model):
    venue_id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String, nullable = False)
    place = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(), nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    show = db.relationship('Shows', backref='venue_1',
                           cascade = 'all, delete', 
                           primaryjoin = 'Shows.venue==Venues.venue_id')
    booking = db.relationship('Bookings', backref = 'venue_2',
                              cascade = 'all, delete',
                              primaryjoin = 'Bookings.venue ==Venues.venue_id')

    pass

class Shows(db.Model):
    show_id = db.Column(db.Integer(), primary_key = True,autoincrement=True)
    venue = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    movie = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    show_name = db.Column(db.String(), nullable = False)
    show_date = db.Column(db.String(), nullable = False)
    show_time = db.Column(db.String(), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    booking = db.relationship('Bookings', backref = 'show_1',
                              cascade = 'all, delete',
                              primaryjoin = 'Bookings.show ==Shows.show_id')

    pass

class Bookings(db.Model):
    booking_id = db.Column(db.Integer, primary_key = True)
    venue = db.Column(db.Integer(), db.ForeignKey('venues.venue_id')) 
    user = db.Column(db.Integer(),db.ForeignKey('users.user_id'))
    movie = db.Column(db.Integer(), db.ForeignKey('movies.movie_id'))
    show = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    booking_count = db.Column(db.Integer(), nullable = False)
    total = db.Column(db.Integer(), nullable = False)
    canceled = db.Column(db.Boolean, default= False)
    pass

