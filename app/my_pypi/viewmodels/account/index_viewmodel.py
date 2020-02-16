from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase
from my_pypi.services import user_service

class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user = user_service.find_user_by_id(self.user_id)