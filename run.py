from project.config import config
from project.models import Genre, Director, User, Movie
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "User": User,
        "Movie": Movie,
        "Director": Director
    }


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
