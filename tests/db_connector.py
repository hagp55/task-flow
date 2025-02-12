from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import db

test_engine: Engine = create_engine(url=db.DNS_DB)
test_session_factory = sessionmaker(bind=test_engine)
