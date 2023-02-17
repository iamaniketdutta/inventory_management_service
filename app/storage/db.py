from configuration.constants import Common, Numeric
from simple_settings import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from utilities.singleton_utils import Singleton


class DbManager(metaclass=Singleton):
    def __init__(
        self,
        username=settings.username,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database_name=settings.database_name,
    ) -> None:
        url_object = URL.create(
            "mysql",
            username=username,
            password=password,
            host=host,
            database=database_name,
        )
        self.engine = create_engine(
            url_object, pool_size=settings.DATABASE_POOL_SIZE, pool_pre_ping=True
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def paginate(self, query, page_number, page_limit):
        length = query.count()
        if page_number:
            query = query.offset((page_number - Numeric.ONE.value) * page_limit)
        if page_limit:
            query = query.limit(page_limit)
        return {Common.COUNT.value: length, Common.DATA.value: query.all()}
