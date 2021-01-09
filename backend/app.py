import os
from lib.app import create_app
from lib.config import env

os.environ['FLASK_ENV'] = env.TRADER_RIMPO_ENV

debug = True if env.TRADER_RIMPO_ENV in [env.TESTING, env.DEVELOPMENT] else False
print(debug)

app = create_app()

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port='5000')
