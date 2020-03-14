
import json
import os
import sys
import time
from typing import List, Optional, Dict

import progressbar
from dateutil.parser import parse

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))

from my_pypi.data.users import User
from my_pypi.data.releases import Release
from my_pypi.data.package import Package
from my_pypi.data.maintainers import Maintainer
from my_pypi.data.licenses import License
from my_pypi.data.languages import ProgrammingLanguage
import my_pypi.data.db_session as db_session
from my_pypi.utils.num_convert import try_int
from my_pypi.config import DevelopmentConfig

from my_pypi.services import user_service, package_service, general_service


def main():
    init_db()
    session = db_session.create_session()
    user_count = session.query(User).count()
    session.close()
    
    file_data = do_load_files()
    users = find_users(file_data)

    db_users = do_user_import(users)
    do_import_packages(file_data, db_users)

    do_import_languages(file_data)
    do_import_licenses(file_data)

    do_summary()


def do_import_languages(file_data: List[dict]):
    imported = set()
    print("Importing languages ... ", flush=True)
    pbar = progressbar.ProgressBar(maxval=len(file_data)).start()
    for idx, p in enumerate(file_data):
        info = p.get('info')
        classifiers = info.get('classifiers')
        for c in classifiers:
            if 'Programming Language' not in c:
                continue

            original = c

            c = c.replace('Implementation ::', '').replace('::', ':')
            text = c
            parts = c.split(':')
            if len(parts) > 1:
                text = ' '.join(parts[-2:]).strip().replace('  ', ' ')
            if general_service.get_language_by_id(text):
                pbar.update(idx)
                return
            if text not in imported:
                imported.add(text)
                session = db_session.create_session()

                lang = ProgrammingLanguage()
                lang.description = original
                lang.id = text
                session.add(lang)
                session.commit()

        pbar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()


def do_import_licenses(file_data: List[dict]):
    imported = set()
    print("Importing licenses ... ", flush=True)
    pbar = progressbar.ProgressBar(maxval=len(file_data)).start()
    for idx, p in enumerate(file_data):
        info = p.get('info')
        license_text = detect_license(info.get('license'))
        if general_service.get_licenses_by_id(license_text):
            pbar.update(idx)
            return
        if license_text and license_text not in imported:
            imported.add(license_text)
            session = db_session.create_session()

            package_license = License()
            package_license.id = license_text
            package_license.description = info.get('license')

            session.add(package_license)
            session.commit()

        pbar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()


def do_summary():
    session = db_session.create_session()

    print("Final numbers:")
    print("Users: {:,}".format(session.query(User).count()))
    print("Packages: {:,}".format(session.query(Package).count()))
    print("Releases: {:,}".format(session.query(Release).count()))
    print("Maintainers: {:,}".format(session.query(Maintainer).count()))
    print("Languages: {:,}".format(session.query(ProgrammingLanguage).count()))
    print("Licenses: {:,}".format(session.query(License).count()))


def do_user_import(user_lookup: Dict[str, str]) -> Dict[str, User]:
    print("Importing users ... ", flush=True)
    pbar = progressbar.ProgressBar(maxval=len(user_lookup)).start()
    for idx, (email, name) in enumerate(user_lookup.items()):
        session = db_session.create_session()
        session.expire_on_commit = False
        if session.query(User).filter(User.email == email).first():
           #user exists
           pbar.update(idx)
        else: 
            user = User()
            user.email = email
            user.name = name
            session.add(user)
            session.commit()
        session.close()
        pbar.update(idx)

    print()
    sys.stderr.flush()
    sys.stdout.flush()

    session = db_session.create_session()
    return {u.email: u for u in session.query(User)}


def do_import_packages(file_data: List[dict], user_lookup: Dict[str, User]):
    errored_packages = []
    print("Importing packages and releases ... ", flush=True)
    pbar = progressbar.ProgressBar(maxval=len(file_data)).start()
    for idx, p in enumerate(file_data):
        try:
            load_package(p, user_lookup)
            pbar.update(idx)
        except Exception as x:
            errored_packages.append(
                (p, " *** Errored out for package {}, {}".format(p.get('package_name'), x)))
            raise
    sys.stderr.flush()
    sys.stdout.flush()
    print()
    print("Completed packages with {} errors.".format(len(errored_packages)))
    for (p, txt) in errored_packages:
        print(txt)


def do_load_files() -> List[dict]:
    data_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../data/pypi-packages'))
    print("Loading files from {}".format(data_path))
    files = get_file_names(data_path)
    print("Found {:,} files, loading ...".format(len(files)), flush=True)
    time.sleep(.1)

    file_data = []
    pbar = progressbar.ProgressBar(maxval=len(files)).start()
    for idx, f in enumerate(files):
        file_data.append(load_file_data(f))
        pbar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()
    print()
    return file_data


def find_users(data: List[dict]) -> dict:
    print("Discovering users...", flush=True)
    found_users = {}
    pbar = progressbar.ProgressBar(maxval=len(data)).start()
    for idx, p in enumerate(data):
        info = p.get('info')
        found_users.update(get_email_and_name_from_text(
            info.get('author'), info.get('author_email')))
        found_users.update(get_email_and_name_from_text(
            info.get('maintainer'), info.get('maintainer_email')))
        pbar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()
    print()
    print("Discovered {:,} users".format(len(found_users)))
    print()

    return found_users


def get_email_and_name_from_text(name: str, email: str) -> dict:
    data = {}

    if not name or not email:
        return data

    emails = email.strip().lower().split(',')
    names = name
    if len(email) > 1:
        names = name.strip().split(',')

    for n, e in zip(names, emails):
        if not n or not e:
            continue

        data[e.strip()] = n.strip()

    return data


def load_file_data(filename: str) -> dict:
    try:
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            if not data.get('package_name', '').strip():
                data['package_name'] = os.path.basename(filename).split('.')[0]
    except Exception as x:
        print("ERROR in file: {}, details: {}".format(filename, x), flush=True)
        raise

    return data


def load_package(data: dict, user_lookup: Dict[str, User]):
    try:
        info = data.get('info', {})

        p = Package()
        p.id = data.get('package_name', '').strip()
        if not p.id:
            return

        if package_service.get_package_by_id(p.id):
            return

        p.author = info.get('author')
        p.author_email = info.get('author_email')

        releases = build_releases(p.id, data.get("releases", {}))

        if releases:
            p.created_date = releases[0].created_date

        maintainers_lookup = get_email_and_name_from_text(
            info.get('maintainer'), info.get('maintainer_email'))
        maintainers = []
        for email, name in maintainers_lookup.items():
            user = user_lookup.get(email)
            if not user:
                continue

            m = Maintainer()
            m.package_id = p.id
            m.user_id = user.id
            maintainers.append(m)

        p.summary = info.get('summary')
        p.description = info.get('description')

        p.home_page = info.get('home_page')
        p.docs_url = info.get('docs_url')
        p.package_url = info.get('package_url')

        p.author = info.get('author')
        p.author_email = info.get('author_email')
        p.license = detect_license(info.get('license'))

        session = db_session.create_session()
        session.add(p)
        session.add_all(releases)
        if maintainers:
            session.add_all(maintainers)
        session.commit()
        session.close()
    except OverflowError:
        # What the heck, people just putting fake data in here
        # Size is terabytes...
        pass
    except Exception:
        raise


def detect_license(license_text: str) -> Optional[str]:
    if not license_text:
        return None

    license_text = license_text.strip()

    if len(license_text) > 100 or '\n' in license_text:
        return "CUSTOM"

    license_text = license_text \
        .replace('Software License', '') \
        .replace('License', '')

    if '::' in license_text:
        # E.g. 'License :: OSI Approved :: Apache Software License'
        return license_text \
            .split(':')[-1] \
            .replace('  ', ' ') \
            .strip()

    return license_text.strip()


def build_releases(package_id: str, releases: dict) -> List[Release]:
    db_releases = []
    for k in releases.keys():
        all_releases_for_version = releases.get(k)
        if not all_releases_for_version:
            continue

        v = all_releases_for_version[-1]

        r = Release()
        r.package_id = package_id
        r.major_ver, r.minor_ver, r.build_ver = make_version_num(k)
        r.created_date = parse(v.get('upload_time'))
        r.comment = v.get('comment_text')
        r.url = v.get('url')
        r.size = int(v.get('size', 0))

        db_releases.append(r)

    return db_releases


def make_version_num(version_text):
    major, minor, build = 0, 0, 0
    if version_text:
        version_text = version_text.split('b')[0]
        parts = version_text.split('.')
        if len(parts) == 1:
            major = try_int(parts[0])
        elif len(parts) == 2:
            major = try_int(parts[0])
            minor = try_int(parts[1])
        elif len(parts) == 3:
            major = try_int(parts[0])
            minor = try_int(parts[1])
            build = try_int(parts[2])

        return major, minor, build


def init_db():
    db_session.global_init(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, False)#TODO: Make it better

def get_file_names(data_path: str) -> List[str]:
    files = []
    for f in os.listdir(data_path):
        if f.endswith('.json'):
            files.append(
                os.path.abspath(os.path.join(data_path, f))
            )

    files.sort()
    return files


if __name__ == '__main__':
    main()
