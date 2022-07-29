from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссеры', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Быков'),
})

movie: Model = api.model('Фильмы', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Джанго освобожденный'),
    'description': fields.String(required=True, max_length=100,
                                 example='Эксцентричный охотник за головами, также известный как Дантист, промышляет отстрелом самых опасных преступников. Работенка пыльная, и без надежного помощника ему не обойтись. Но как найти такого и желательно не очень дорогого? Освобождённый им раб по имени Джанго – прекрасная кандидатура. Правда, у нового помощника свои мотивы – кое с чем надо сперва разобраться.'),
    'trailer': fields.String(required=True, max_length=100, example='https://www.youtube.com/watch?v=2Dty-zwcPv4'),
    'year': fields.String(required=True, example=2012),
    'rating': fields.String(required=True, example=8.4),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='mar@mail.ru'),
    'password': fields.String(required=True, example='156156'),
    'name': fields.String(required=True, example='Maria'),
    'surname': fields.String(required=True, example='Yashina'),
    'favorite_genre_rel': fields.Nested(genre)
})

favorite_movie: Model = api.model('Избранные фильмы', {
    'id': fields.Integer(required=True, example=1),
    'user_idr': fields.Nested(user),
    'movie_idr': fields.Nested(movie)
})
