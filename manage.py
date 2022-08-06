import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler

from app_main import app, db
from utils import update_db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def updated():
    return update_db(1)


if __name__ == '__main__':
    sched = BackgroundScheduler()
    sched.add_job(updated, 'cron', hour=12, minute=59)
    sched.start()
    manager.run()
