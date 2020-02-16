import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from my_pypi.data.modelbase import SqlAlchemyBase
#Singleton
__factory = None


def global_init(db_url: str, drop_all: bool):#TODO: Make it better
    global __factory

    if __factory:
        return

    engine = sa.create_engine(db_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    import my_pypi.data.__all_models
    if drop_all:
        SqlAlchemyBase.metadata.drop_all(engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    session: Session = __factory()
    session.expire_on_commit = False
    return __factory()
