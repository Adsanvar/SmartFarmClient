from flask import Flask
import logging
import datetime
try:
    ##Creates the Flask Application with the configurations -Adrian
    def create_app():
        now = datetime.datetime.now()
        logging.basicConfig(filename = '{}.log'.format(now.date()), level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        app = Flask(__name__)
        #allows us to use Login Manager and other tools suchas Flash from flask_login - Adrian
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['SCHEDULER_API_ENABLED'] = True
        
        #blueprints for the pages and models - Adrian
        from SmartLock.web_server import home as h_bp
        
        app.register_blueprint(h_bp)
        app.logger.info('App Launched')
        return app
except:
    app = create_app()
    app.logger.error('App Failed To Launch')
    raise
