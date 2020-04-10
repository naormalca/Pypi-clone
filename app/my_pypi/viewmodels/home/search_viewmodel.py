from my_pypi.services import user_service, package_service
from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase


class SearchViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.query = self.request.args['query']
        if self.query:
            self.packages = package_service.search_packages_by_keyword(self.query)
            self.amount_of_packages = len(self.packages)