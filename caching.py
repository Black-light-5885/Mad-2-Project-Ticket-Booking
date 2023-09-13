from cache_ import cache
from models import *
import base64

@cache.cached(timeout=1800, key_prefix="get_venues")
def get_venue():
    theaters = Venues.query.all()
    theater_list = []
    for theater in theaters:
        shows = Shows.query.filter_by(venue= theater.venue_id).all()
        theater_list.append({'name':theater.venue_name,
                                "place": theater.place,
                                'location':theater.location,
                                'capacity':theater.capacity,
                                'id':theater.venue_id,
                                "shows_count":len(shows)})
    return theater_list

@cache.cached(timeout=100, key_prefix="get_movies")
def get_movies():
    movies = Movies.query.all()
    movie_list = []
    for movie in movies:
        if movie.rating>0:
            rating = round(movie.rating/movie.rating_count,2)
        else:
            rating =0
        movie_list.insert(0,{'title':movie.movie_name,'id':movie.movie_id,
                            'tags':movie.tags,'rating':rating, "lang":movie.language,
                            'r_count':movie.rating_count,
                            'picture': base64.b64encode(movie.picture).decode('utf-8')})
    return movie_list

@cache.memoize(timeout=1800)
def get_show_one(s_id):
    show = Shows.query.get(int(s_id))
    theater  = Venues.query.filter_by(venue_id = show.venue).first()
    movie = Movies.query.filter_by(movie_id = show.movie).first()
    bookings = Bookings.query.filter_by(show=show.show_id).all()
    booked = 0
    for bk in bookings:
            booked +=bk.booking_count
    if theater.capacity - booked <50:
        price = show.price*1.20
    else:
        price = show.price
    show_list={'name':show.show_name,
                    'id':show.show_id,
                    "price":price,
                    "date":show.show_date,
                    "time":show.show_time,
                    "location":theater.location,
                    "place":theater.place,
                    "theater_id":theater.venue_id,
                    "movie_id":movie.movie_id,
                    'movie':movie.movie_name,
                    'theater': theater.venue_name,
                    'available':theater.capacity-booked}
    return show_list

@cache.cached(timeout=1800, key_prefix="get_all_show")
def get_all_show():
    shows = Shows.query.all()
    show_list = []
    for show in shows:
        theater  = Venues.query.filter_by(venue_id = show.venue).first()
        movie = Movies.query.filter_by(movie_id = show.movie).first()
        bookings = Bookings.query.filter_by(show=show.show_id).all()
        booked = 0
        for bk in bookings:
            booked +=bk.booking_count
        if theater.capacity - booked <50:
            price = show.price*1.20
        else:
            price = show.price
        show_list.insert(0,{'name':show.show_name,
                        'id':show.show_id,
                        "price":price,
                        "date":show.show_date,
                        "place":theater.place,
                        "time":show.show_time,
                        "location":theater.location,
                        "theater_id":theater.venue_id,
                        "movie_id":movie.movie_id,
                        'movie':movie.movie_name,
                        'theater': theater.venue_name,
                        'available':theater.capacity-booked})
    return show_list

@cache.memoize( timeout=1800)
def get_user_bookings(user_name):
    user = Users.query.filter_by(user_name = user_name).first()
    u_id = user.user_id
    bookings = Bookings.query.filter_by(user = u_id).all()
    booking_list = []
    for booking in bookings:
        if not booking.canceled:
            show = Shows.query.get(booking.show)
            theater = Venues.query.get(booking.venue)
            movie = Movies.query.get(booking.movie)
            booking_list.insert(0,
                                {'show_name':show.show_name,'id':booking.booking_id,
                                    'time':show.show_time,
                                    'date':show.show_date,
                                    'price':show.price,
                                    'movie': movie.movie_name,
                                    "theater": theater.venue_name,
                                    'location': theater.location,
                                    'count': booking.booking_count,
                                    'total': booking.total})
    return booking_list

def clear_cache(key=None):
    if key:
        cache.delete(key)
    else:
        cache.clear()