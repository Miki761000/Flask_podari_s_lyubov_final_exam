from config import create_app
from db import db

app = create_app()


@app.before_first_request
def init_request():
    db.init_app(app)


if __name__ == "__main__":
    app.run()
