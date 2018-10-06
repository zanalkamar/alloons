from src.app import app
from src.common.database import Database

Database.initialize()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4904)











