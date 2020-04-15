from typing import List, Optional
import sqlalchemy.orm
from sqlalchemy import or_

import my_pypi.data.db_session as db_session
from my_pypi.data.package import Package
from my_pypi.data.releases import Release


def get_latest_releases(limit=10) -> List[Release]:
    session = db_session.create_session()

    releases = session.query(Release). \
        options(sqlalchemy.orm.joinedload(Release.package)). \
        order_by(Release.created_date.desc()). \
        limit(limit). \
        all()

    session.close()

    return releases


def get_package_count() -> int:
    session = db_session.create_session()
    return session.query(Package).count()


def get_release_count() -> int:
    session = db_session.create_session()
    return session.query(Release).count()


def get_package_by_id(package_id: str) -> Optional[Package]:
    if not package_id:
        return None

    package_id = package_id.strip().lower()

    session = db_session.create_session()

    package = session.query(Package) \
        .options(sqlalchemy.orm.joinedload(Package.releases)) \
        .filter(Package.id == package_id) \
        .first()

    session.close()

    return package

def search_packages_by_keyword(query: str) -> List[Package]:
    if not query:
        return None

    query = query.strip().lower()
    session = db_session.create_session()

    search = "%{}%".format(query)

    packages_found_title = session.query(Package) \
        .filter(or_(Package.id.like(search), Package.description.like(search)))
    
    return packages_found_title
