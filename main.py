from flask import Flask, render_template
import config
from models import *
from api import api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from flask_requests import request
from celery_worker import make_celery
from flask_mail import Mail


app = Flask(__name__, static_folder='./static')
api.init_app(app)
app.config.from_object(config)
db.init_app(app)
celery = make_celery(app)
jwt = JWTManager(app)
mail = Mail(app)
CORS(app)
app.app_context().push()


from cache_ import cache
cache.init_app(app)
app.app_context().push()

db.create_all()
a = Users.query.get(1)
if not a:
    au = Users(full_name='Admin', user_name = 'admin1', password = 'Bala1234',email = 'bala@gmail.com',admin = True)
    u = Users(full_name='user', user_name = 'user1', password = 'Bala1234',email = 'bala1@gmail.com',admin = False)
    db.session.add(au)
    db.session.add(u)
    db.session.commit()

@app.route('/Apphome')
def home_():
    return render_template('index.html')

from workers import *
@app.route('/admin/export_csv')
@jwt_required()
def export_csv():
    booking_summary.delay()
    return {'message':"Exporting Bookings as .csv file. You will receive an email once the process is complete."}


if __name__ == '__main__':
    app.run(debug=True)

