import os,sys
from flask.cli import FlaskGroup

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from my_pypi.app import create_app
from my_pypi.bin import load_data


cli = FlaskGroup(create_app())


@cli.command("load_db")
def create_db():
    load_data.load(True)


if __name__ == "__main__":
    cli()