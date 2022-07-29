from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api.models import director
from project.setup.api.parsers import page_parser

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        return movie_service.get_all(**page_parser.parse_args())


@api.route('/<int:director_id>/')
class DirectorsView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(director, code=200, description='OK')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        return movie_service.get_item(director_id)
