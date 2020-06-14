import flask
from flask import make_response
from flask_cors import cross_origin
from my_pypi.services import package_service, user_service
from my_pypi.data.schemas import ReleaseSchema

blueprint = flask.Blueprint(
    'api_packages', __name__, url_prefix='/api/packages')

QUERY_LIMIT = 40


@blueprint.route('/stats')
@cross_origin()
def get_packages_stats():
    package_count = package_service.get_package_count()
    release_count = package_service.get_release_count()
    user_count = user_service.get_user_count()

    response_obj = {'packages': package_count,
                    'releases': release_count, 'users': user_count}
    return response_obj


@blueprint.route('/latest-releases/<int:amount>')
@cross_origin()
def get_latest_releases(amount: int):
    if amount > QUERY_LIMIT:
        amount = QUERY_LIMIT

    releases = package_service.get_latest_releases(amount)
    releases_schema = ReleaseSchema(many=True)

    response_obj = releases_schema.dumps(releases) 
    return response_obj
