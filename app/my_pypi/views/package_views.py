import flask

from my_pypi.infrastructure.view_modifiers import response
from my_pypi.viewmodels.package.pagedetails_viewmodel import PackageDetailsViewModel

blueprint = flask.Blueprint('packages', __name__, template_folder='templates')


@blueprint.route('/project/<package_name>')
@response(template_file='packages/details.html')
def package_details(package_name: str):
    vm = PackageDetailsViewModel(package_name)
    if not package_name:
        return flask.abort(status=404)
    return vm.to_dict()


@blueprint.route('/<int:rank>')
def popular(rank: int):
    print(type(rank), rank)
    return "The details for the {}th most popular package".format(rank)
