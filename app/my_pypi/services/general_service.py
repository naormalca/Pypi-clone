from typing import Optional

from my_pypi.data.languages import ProgrammingLanguage
from my_pypi.data.licenses import License
import my_pypi.data.db_session as db_session



def get_language_by_id(lang_id: str) -> Optional[ProgrammingLanguage]:
    session = db_session.create_session()
    lang = session.query(ProgrammingLanguage) \
        .filter(ProgrammingLanguage.id == lang_id).first()
    session.close()
    return lang

def get_licenses_by_id(licenses_id: str) -> Optional[License]:
    session = db_session.create_session()
    lic = session.query(License) \
        .filter(License.id == licenses_id).first()
    session.close()
    return lic