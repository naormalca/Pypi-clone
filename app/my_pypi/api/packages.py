import flask
from flask_cors import cross_origin
from my_pypi.services import package_service, user_service
from my_pypi.data.empty_object import Object
from my_pypi.data.schemas import ReleaseSchema, PackageDetailsSchema

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
    return response_obj, 200


@blueprint.route('/latest-releases/<int:amount>')
@cross_origin()
def get_latest_releases(amount: int):
    if amount > QUERY_LIMIT:
        amount = QUERY_LIMIT

    releases = package_service.get_latest_releases(amount)
    releases_schema = ReleaseSchema(many=True)

    response_obj = releases_schema.dumps(releases) 
    return response_obj, 200

@blueprint.route('/<string:package_id>')
@cross_origin()
def get_package_details(package_id: str):
    package = package_service.get_package_by_id(package_id)
    if package:
        #get only the latest release
        latest_release = package.releases[0]
        #create an object to represent the package details
        package_details = Object()
        package_details.package = package
        package_details.latest_release = latest_release
        #dumps to a schema
        package_details_schema = PackageDetailsSchema()
        response_obj = package_details_schema.dumps(package_details)
        return response_obj, 200

    else:
        response_obj = {
            'error': 'Package not exists'
        }
        return response_obj, 202
