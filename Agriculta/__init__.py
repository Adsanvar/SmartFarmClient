from flask import Flask
import logging
import datetime
from pathlib import Path
try:
    ##Creates the Flask Application with the configurations -Adrian
    def create_app():
        now = datetime.datetime.now()
        Path("logs").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename = '{}/{}.log'.format('logs', now.date()), level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        app = Flask(__name__)
        #allows us to use Login Manager and other tools suchas Flash from flask_login - Adrian
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['SCHEDULER_API_ENABLED'] = True
        
        #blueprints for the pages and models - Adrian
        from Agriculta.web_server import home as h_bp
        
        app.register_blueprint(h_bp)
        app.logger.info('App Launched')
        return app
except:
    app = create_app()
    app.logger.error('App Failed To Launch')
    raise
