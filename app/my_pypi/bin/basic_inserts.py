import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))

import my_pypi.data.db_session as db_session
from my_pypi.data.package import Package
from my_pypi.data.releases import Release
from my_pypi.config import DevelopmentConfig

def main():
    init_db()
    while True:
        insert_a_package()


def insert_a_package():
    p = Package()
    p.id = input('Package id / name: ').strip().lower()

    p.summary = input("Package summary: ").strip()
    p.author_name = input("Author: ").strip()
    p.license = input("License: ").strip()

    print("Release 1:")
    r = Release()
    r.major_ver = int(input("Major version: "))
    r.minor_ver = int(input("Minor version: "))
    r.build_ver = int(input("Build version: "))
    r.size = int(input("Size in bytes: "))
    p.releases.append(r)

    print("Release 2:")
    r = Release()
    r.major_ver = int(input("Major version: "))
    r.minor_ver = int(input("Minor version: "))
    r.build_ver = int(input("Build version: "))
    r.size = int(input("Size in bytes: "))
    p.releases.append(r)

    session = db_session.create_session()
    session.add(p)
    session.commit()


def init_db():
    db_session.global_init(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)


if __name__ == '__main__':
    main()
