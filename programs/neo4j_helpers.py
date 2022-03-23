from contextlib import contextmanager
from typing import List, Tuple, Dict

from neo4j import GraphDatabase


@contextmanager
def open_session(url: str, db: str):
    driver = GraphDatabase.driver(url)
    session = driver.session(database=db)
    try:
        yield session
    finally:
        session.close()
        driver.close()


def run_script(db_url: str, db: str, script_path: str):
    with open(script_path, mode='r', encoding='utf8') as script:
        queries = [query.strip() for query in script.read().split('//--')]
        run_queries(db_url, db, queries)


def run_queries(db_url: str, db: str, queries: List[str | Tuple[str, str] | Tuple[str, str, Dict[str, str]]]):
    with open_session(db_url, db) as session:
        for q in queries:
            if isinstance(q, str):
                print('Running query', '...', end=' ')
                session.run(q)
                print('Done')
            else:
                if len(q) == 3:
                    name, query, params = q
                else:
                    name, query = q
                    params = {}
                print(name, '...', end=' ')
                session.run(query, **params)
                print('Done')
