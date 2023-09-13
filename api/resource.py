from flask_restful import Resource,fields,marshal_with
from flask import request,jsonify
from models import *
from flask_jwt_extended import jwt_required,create_access_token
from .validation import *
from caching import *
import datetime


user_output = {
                "user_id" : fields.Integer,
                "user_name" : fields.String,
                "full_name" : fields.String,
                "last_login" : fields.String,
                "email" : fields.String,
                "admin": fields.Boolean

            }

movie_output = {
                "movie_id" : fields.Integer,
                "movie_name" : fields.String,
                "tags" : fields.String,
                "rating"  : fields.Float,
                "rating_count" : fields.Float,
                "language" : fields.String,

            }


class Login(Resource):
    def post(self):
        data = request.get_json()
        user_name = data['user_name']
        password = data['password']
        l_login = datetime.datetime.now()
        user = Users.query.filter_by(user_name=user_name).first()
        if user:
            if user.password == password:
                admin = user.admin
                user.last_login  = l_login
                db.session.add(user)
                db.session.commit()
                token = create_access_token(identity=user.user_id)
                return jsonify({'token':token,
                                'admin':admin})
            else:
                print('adsf')
                raise BusninessValidationError(status_code=400,error_message='Full Name Empty or Too short')
        else:
            raise NotFoundError(404)
    pass


class AdminData(Resource):
    @jwt_required()
    def get(self):
        data= []
        label = []
        movie_dic = {}
        bookings = Bookings.query.all()
        movies = Movies.query.all()
        theatres = Venues.query.all()
        shows = Shows.query.all()
        card_data = {'booking':len(bookings),
                     "movie": len(movies),
                     'theatre': len(theatres),
                     'show': len(shows)}
        for booking in bookings:

            movie = Movies.query.get(booking.movie)
            theatre = Venues.query.get(booking.venue)
            user = Users.query.get(booking.user)
            show = Shows.query.get(booking.show)
            print(movie)
            if movie.movie_name not in movie_dic.keys():
                movie_dic[movie.movie_name] = booking.booking_count
            else:
                movie_dic[movie.movie_name] += booking.booking_count
        for movie in movie_dic:
            data.append(movie_dic[movie])
            label.append(movie)
        print(label)
        data = {'count':data, 'lables':label, "card_data":card_data}
        response = make_response(jsonify(data))
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

class UserApi(Resource):
    @marshal_with(user_output)
    @jwt_required()
    def get(self,user_name):
        user = Users.query.filter_by(user_name = user_name).first()
        return user
    
    @jwt_required()
    def delete(self, user_name):
        user = Users.query.filter_by(user_name = user_name).first()
        if user:
            db.session.delete(user)
            db.session.commint()
            return "Deleted successfully"
        else:
            raise NotFoundError(404)
  
    def post(self):
        user_data  = request.get_json()
        full_name = user_data['full_name']
        user_name = user_data['user_name']
        email = user_data['email']
        password = user_data['password']
        admin = bool(user_data['admin'])
        user_ = Users.query.filter_by(user_name=user_name).first()
        if full_name =='None' or len(full_name)<=2:
            raise BusninessValidationError(status_code=400,error_message='Full Name Empty or Too short')
        elif user_name == 'None' or len(user_name)<=2:
            raise BusninessValidationError(status_code=400,error_message='User Name Empty or Too short')
        elif user_:
            raise BusninessValidationError(status_code=400,error_message='User Name already used!')

        elif not password:
            raise BusninessValidationError(status_code=400,error_message='Password can\'t empty')
        elif len(password)<7:
            raise BusninessValidationError(status_code=400,error_message='Password length is short. Password must greater than 7')
        else:
            user = Users(user_name=user_name,full_name = full_name,
                         email = email,
                         password = password,
                         admin = admin)
            db.session.add(user)
            db.session.commit()
            return 'user created successfully',201
            pass

class VenueApi(Resource):
    @jwt_required()
    def get(self,t_id=None):
        if t_id:
            theater = Venues.query.get(int(t_id))
            a = {'name':theater.venue_name,
                                "place": theater.place,
                                'location':theater.location,
                                'capacity':theater.capacity,
                                'id':theater.venue_id,
                             }
            return a
        else:
            theater_list = get_venue()
            data = {'theaters':theater_list}
            response = make_response(jsonify(data))
            response.headers.add("Access-Control-Allow-Origin","*")
            return response
        pass
    @jwt_required()
    def put(self,t_id):
        theater = Venues.query.get(int(t_id))
        data = request.get_json()
        theater.venue_name = data['name']
        theater.place = data['place']
        theater.location = data['location']
        theater.capacity = int(data['capacity'])
        db.session.add(theater)
        db.session.commit()
        clear_cache("get_venues")
        return "success"
        pass
    @jwt_required()
    def delete(self,t_id):
        theater = Venues.query.get(int(t_id))
        if theater:
            db.session.delete(theater)
            db.session.commit()
            clear_cache("get_venues")
            return "Deleted successfully", 202
        else:
            return 'Something went wrong', 204
        pass
    @jwt_required()
    def post(self):
        data = request.get_json()
        theater_name = data['name']
        place = data['place']
        location = data['location']
        capacity = int(data['capacity'])
        theater = Venues(venue_name=theater_name,
                         place = place,
                         location = location,
                         capacity = capacity)
        db.session.add(theater)
        db.session.commit()
        clear_cache("get_venues")
        return "Theater created successfully",201
    
        pass

class MovieApi(Resource):
    @jwt_required()
    def get(self):
        movie_list = get_movies()
        data = {'movies':movie_list}
        response = make_response(jsonify(data))
        response.headers.add("Access-Control-Allow-Origin","*")
        return response

    @jwt_required()
    def put(self,m_id):
        data = request.get_json()
        rating = data['rating']
        movie = Movies.query.get(int(m_id))
        movie.rating += int(rating)
        movie.rating_count +=1
        db.session.add(movie)
        db.session.commit()
        clear_cache("get_movies")
        return "",201
        pass
    @jwt_required()
    def delete(self,m_id):
        movie_id = m_id
        movie = Movies.query.get(int(movie_id))
        if movie:
            db.session.delete(movie)
            db.session.commit()
            clear_cache("get_movies")
            return 'Deleted successfully', 202
        else:
            return 'Something is wrong',204

    @jwt_required()
    def post(self):
        movie_data = request.form.to_dict()
        data = movie_data.get('data')
        movie = json.loads(data)
        title = movie.get('name')
        tag = movie.get('tag')
        lang = movie.get('lang')
        image = request.files.get('picture')
        new_movie = Movies(movie_name=title,
                           tags = tag, language = lang, rating_count = 0,
                           rating = 0,
                           picture = image.read())
        db.session.add(new_movie)
        db.session.commit()
        clear_cache("get_movies")
        return "Movie created successfully",201

class ShowApi(Resource):
    @jwt_required()
    def get(self, s_id=None):
        if s_id:
            show_list=get_show_one(s_id=s_id)
            data = {'shows':show_list}
            response = make_response(jsonify(data))
            response.headers.add("Access-Control-Allow-Origin","*")
            return response
        else:
            show_list = get_all_show()
            data = {'shows':show_list}
            response = make_response(jsonify(data))
            response.headers.add("Access-Control-Allow-Origin","*")
            return response
    @jwt_required()
    def delete(self,s_id):
        show = Shows.query.get(int(s_id))
        if show:
            db.session.delete(show)
            db.session.commit()
            clear_cache("get_all_show")
            return "Deleted successfully", 202
        else:
            raise NotFoundError(205)
        pass
    @jwt_required()
    def post(self):
        data = request.get_json()
        show_time = data['show_time']
        show_date = data['date']
        theater = data['theater']
        movie = data['movie']
        show_name = data['show_name']
        price = int(data['price'])
        theater_ = Venues.query.filter_by(venue_name =theater).first()
        movie_ = Movies.query.filter_by(movie_name =movie).first()
        show = Shows(venue = theater_.venue_id,
                     movie = movie_.movie_id,
                     show_name = show_name,
                     show_time = show_time,
                     show_date = show_date,
                     price = price)
        db.session.add(show)
        db.session.commit()
        clear_cache("get_all_show")
        return "show created successfully!",201
        pass




    pass

class BookingApi(Resource):
    @jwt_required()
    def get(self,user_name = None):
        if user_name:
            booking_list = get_user_bookings(user_name)
            data = {'bookings':booking_list}
            response = make_response(jsonify(data))
            response.headers.add("Access-Control-Allow-Origin","*")
            return response
        else:
            return "",204
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = Users.query.filter_by(user_name = data['user']).first()
        movie = Movies.query.filter_by(movie_name = data['movie']).first()
        theater = Venues.query.filter_by(venue_name = data['theater']).first()
        total = data['total']
        show_id = int(data['show'])
        count = int(data['count'])
        booking = Bookings(user = user.user_id,
                           venue = theater.venue_id,
                           movie = movie.movie_id,
                           show =show_id,
                           booking_count = count,
                           total = total)
        db.session.add(booking)
        db.session.commit()
        clear_cache()
        return "Booking successfull ", 201
        pass

class BookingApi2(Resource):
    @jwt_required()
    def delete(self,b_id=None):

        if b_id:
            booking = Bookings.query.get(int(b_id))
            booking.canceled = True
            db.session.add(booking)
            db.session.commit()
            clear_cache()
            return "Deleted successfully",202
        else:
            
            raise NotFoundError(205)
        pass
    
class MovieEdit(Resource):
    @marshal_with(movie_output)
    def get(self,m_id):
        movie = Movies.query.get(int(m_id))
        return movie
        pass
    def put(self, m_id):
        movie = Movies.query.get(int(m_id))
        data = request.get_json()
        movie.movie_name = data['name']
        movie.tags = data['tag']
        movie.language = data['lang']
        db.session.add(movie)
        db.session.commit()
        clear_cache('get_movies')
        return "Success"


