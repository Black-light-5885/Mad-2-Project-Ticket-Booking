from flask_restful import Api




api = Api()

from .resource import  *
api.add_resource(Login,'/app/api/login')
api.add_resource(UserApi,'/app/api/user','/app/api/user/<string:user_name>')
api.add_resource(MovieApi,'/app/api/movie','/app/api/movie/<string:m_id>')
api.add_resource(VenueApi,'/app/api/theater','/app/api/theater/<string:t_id>')
api.add_resource(ShowApi,'/app/api/show','/app/api/show/<string:s_id>')
api.add_resource(BookingApi,'/app/api/bookings','/app/api/bookings/<string:user_name>')
api.add_resource(BookingApi2,'/app/api/booking/<string:b_id>')
api.add_resource(AdminData,'/app/api/adminData')
api.add_resource(MovieEdit,'/app/api/Editmovie/<m_id>')

