from my_pypi.services import user_service
from my_pypi.viewmodels.shared.viewmodelbase import ViewModelBase


class StatsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.new_users = user_service.get_new_users()
        self.latest_logged = user_service.get_latest_logged()
