from sqlalchemy_pagination import paginate

from my_pypi.services import user_service, package_service
from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase

MAX_PAGE_RESULTS = 5

class SearchViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.query = self.request.args['query']
        self.page = self.request.args.get('page', 1, type=int)
        packages_obj = package_service.search_packages_by_keyword(self.query)
        
        packages_page = paginate(packages_obj, self.page, MAX_PAGE_RESULTS)
        if self.query:
            self.packages = packages_page.items
            if packages_page.has_previous:
                self.prv_page_num = packages_page.previous_page
            if packages_page.has_next:
                self.next_page_num = packages_page.next_page
            self.pages = packages_page.pages
        
        