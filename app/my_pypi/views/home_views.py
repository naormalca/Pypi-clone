import flask

from my_pypi.infrastructure.view_modifiers import response
import my_pypi.services.package_service as package_service
import my_pypi.services.user_service as user_service
from my_pypi.viewmodels.home.index_viewmodel import IndexViewModel
from my_pypi.viewmodels.home.search_viewmodel import SearchViewModel
from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    vm = IndexViewModel()
    return vm.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    vm = ViewModelBase()
    return vm.to_dict()

@blueprint.route('/search')
@response(template_file='home/search.html')
def search():
    vm = SearchViewModel()
    
    if len(vm.packages) > 0 and vm.page > vm.pages or vm.page < 0:
        return flask.abort(status=404)

    return vm.to_dict()

