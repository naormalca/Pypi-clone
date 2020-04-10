from typing import List, Optional
import sqlalchemy.orm

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
    #give priority to packages with the query string inside the id
    packages_found_title = session.query(Package) \
        .filter(Package.id.like(search)).all()
    #then the packages with the query inside the description
    packages_found_desc = session.query(Package) \
        .filter(Package.description.like(search)).all()
    print(packages_found_desc)
    #append the lists without duplicates
    packages = list(packages_found_title)
    pkg_title_ids = set(pkg.id for pkg in packages_found_title)
    packages.extend(pkg for pkg in packages_found_desc if pkg.id not in pkg_title_ids)
    
    return packages
