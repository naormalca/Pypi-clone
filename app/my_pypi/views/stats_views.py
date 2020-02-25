import flask

from my_pypi.infrastructure.view_modifiers import response
from my_pypi.viewmodels.statistics.stats_viewmodel import StatsViewModel
blueprint = flask.Blueprint('Statistics', __name__, template_folder='templates')


@blueprint.route('/stats')
@response(template_file='statistics/index.html')
def stats_page():
    vm = StatsViewModel()

    return vm.to_dict()
