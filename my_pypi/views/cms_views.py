import flask

from my_pypi.infrastructure.view_modifiers import response
import my_pypi.services.cms_service as cms_service
from my_pypi.viewmodels.cms.page_viewmodel import PageViewModel
blueprint = flask.Blueprint('cms', __name__, template_folder='templates')


@blueprint.route('/<path:full_url>')
@response(template_file='cms/page.html')
def cms_page(full_url: str):
    vm = PageViewModel(full_url)

    if not vm.page:
        return flask.abort(404)

    return vm.to_dict()
