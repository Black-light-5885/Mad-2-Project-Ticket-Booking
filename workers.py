from main import celery,mail
from models import *
from flask_mail import Message
from datetime import timedelta,datetime
import csv
from celery.schedules import crontab
import jinja2



celery.conf.beat_schedule = {
    'send_monthly_report': {
        'task': 'workers.send_monthly_report',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),
    },
    'daily_reminder': {
        'task': 'workers.daily_reminder',
        'schedule': crontab(minute=1),
    },
}
celery.conf.timezone = 'UTC'

@celery.task(name='send_monthly_report')
def send_monthly_report():
    users = Users.query.all()
    month = datetime.now()
    template_loader = jinja2.FileSystemLoader('./')
    temp_env = jinja2.Environment(loader=template_loader)
    temp = temp_env.get_template("report.html")
    month = month.strftime("%B")
    for user in users:
        data ={}
        data['user_name'] = user.user_name
        data['email'] = user.email
        data['month'] = month
        data['bookings'] = []
        bookings = Bookings.query.filter_by(user = user.user_id).all()
        data["book_count"] = len(bookings)
        for book in bookings:
            m = Movies.query.get(book.movie)
            t = Venues.query.get(book.venue)
            s = Shows.query.get(book.show)
            b = {}
            b['id'] = book.booking_id
            b["movie_name"] = m.movie_name
            b["theater"] = t.venue_name
            b["date"] = s.show_date
            b["time"] = s.show_time
            b['count'] = book.booking_count
            b["price"] = s.price
            b['total'] = book.total
            data["bookings"].append(b)
        output = temp.render(data = data)
        msg = Message("BookFor You Reminder",
                          sender="Bookforyou468@gmail.com",
                          recipients=["balamurugan54123@gmail.com"])
        msg.html = output
        mail.send(message=msg)

    return "Monthly Reports sent successfully...!"

@celery.task(name="workers.daily_reminder")
def daily_reminder():
    users = Users.query.all()
    # today  = datetime.now()-timedelta(days=1)
    today  = datetime.now()-timedelta(seconds=10)
    for user in  users:
        l_login = datetime.strptime(user.last_login,"%Y-%m-%d %H:%M:%S.%f")
        if l_login<today:
            msg = Message("BookFor You Reminder",
                          sender="Bookforyou468@gmail.com",
                          recipients=["balamurugan54123@gmail.com"])
            msg.body= f"Hey {user.user_name}! \n Hope you're doing well.\n \
                you haven't booked anything on BOOKFORYOU for past one day"
            mail.send(message=msg)
            pass

    return "reminder send successfully...!"

@celery.task()
def booking_summary():
    col1 = ['Booking ID','Movie_Name', "User",
            "Theatre Name", "Show","Time","No_Bookings","Total", "Status"]
    movie_rows = []
    bookings = Bookings.query.all()
    for booking in bookings:
        movie = Movies.query.get(booking.movie)
        theatre = Venues.query.get(booking.venue)
        user = Users.query.get(booking.user)
        show = Shows.query.get(booking.show)
        movie_rows.append([booking.booking_id,movie.movie_name,user.user_name,
                           theatre.venue_name,
                           show.show_name,
                           show.show_time, booking.booking_count,
                           booking.total, "Canceled" if booking.canceled else "Active"])
    with open("static/movie.csv",'w') as moviefile:
        writer = csv.writer(moviefile)
        writer.writerow(col1)
        writer.writerows(movie_rows)
    with open("static/movie.csv",'r') as moviefile_out:
        msg = Message("Booking Report",recipients=["Balamurugan54123@gmail.com"],
                        sender="No-Reply@bookforyou.com")
        msg.attach('Booking_file.csv',"text/csv",moviefile_out.read())
        date = datetime.today()
        msg.body=f"Hi Admin \nFind the attachment for the {date} date booking csv file."
        mail.send(message= msg)

    return "Export CSV Job Completed...!"
        
@celery.on_after_configure.connect
def reminder(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=9, minute=45), daily_reminder.s(), name = 'Daily Reminder Job')
    sender.add_periodic_task(crontab(hour=9, minute=45), daily_reminder.s(), name = 'Daily Reminder Job')
    sender.add_periodic_task(crontab(day_of_month='23', hour=19, minute=7), send_monthly_report.s(), name = 'Monthly Reminder Job')
    sender.add_periodic_task(10, send_monthly_report.s(), name = 'Monthly Reminder Job')


