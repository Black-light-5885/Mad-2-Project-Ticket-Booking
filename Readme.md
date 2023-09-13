To run the app
install all the dependancies from `requirement.txt` file.
Once all the dependancies installed,
`cd to front_end` and run `npm run serve`
In another terminal `run main.py` file using `python`
In another terminal start a redis `server using sudo service redis-server start` command
In another termianl start a celery worker using c`elery -A application.celery worker` command
In another terminal start the celery beat using `celery -A application.celery beat`

Start using the app.
Thanks