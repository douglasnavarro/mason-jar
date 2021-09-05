from flask import Flask
from flask import render_template

# we wrap this code in a function so it can
# called by tests
def create_app(test_config=None):
    '''
    Creates and configures the app
    '''
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load configuration variables from config.py
        app.config.from_object('config')

        # or redefine the same variables from ../instance/config.py
        # if it exists (development environment)
        try:
            app.config.from_pyfile('config.py')
        except:
            pass
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    from . import api
    app.register_blueprint(api.bp)
    
    return app


