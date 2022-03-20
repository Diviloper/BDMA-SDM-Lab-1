import argparse
import sys
from typing import List

from programs.neo4j_helpers import run_queries


def clean_database(arguments: List[str]):
    parser = argparse.ArgumentParser(description='Delete every node and edge from the database')
    parser.add_argument('-d', '--db', dest='db_url', help='url of the database (default: "bolt://localhost:7687")',
                        default='bolt://localhost:7687')
    parser.add_argument('-n', '--db_name', dest='db_name', help='name of the database, if not provided, chose default')

    args = parser.parse_args(arguments)

    run_queries(args.db_url, args.db_name, [('Deleting everything', 'MATCH (n) DETACH DELETE n;')])


if __name__ == '__main__':
    clean_database(sys.argv[1:])
