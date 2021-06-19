import os
from app import create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from dotenv import load_dotenv


APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
env = os.getenv("FLASK_ENV")


main = create_app(env)
manager = Manager(main)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()