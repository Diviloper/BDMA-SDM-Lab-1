import argparse
import os
import sys
from typing import List

from programs.neo4j_helpers import run_queries, run_script


def load_database(arguments: List[str]):
    parser = argparse.ArgumentParser(description='Creates and loads the database')
    parser.add_argument('-d', '--db', dest='db_url', help='url of the database (default: "bolt://localhost:7687")',
                        default='bolt://localhost:7687')
    parser.add_argument('-n', '--db_name', dest='db_name',
                        help='name of the database, if not provided the default database will be used')
    parser.add_argument('-s', '--script', dest='script_path',
                        help='path of the query script (default: "./program_queries/load.cypher")',
                        default='./program_queries/load.cypher')
    parser.add_argument('-f', '--data_dir', dest='data_dir',
                        help='path of the directory containing data (data, citations and reviewers) csvs. This path'
                             'must be relative to Neo4j import files folder (default: "program_csvs")',
                        default='program_csvs')
    parser.add_argument('--data_csv', dest='data_csv',
                        help='path of the data csv, if not provided <data_dir>/data.csv is used')
    parser.add_argument('--citations_csv', dest='citations_csv',
                        help='path of the citations csv, if not provided <data_dir>/citations.csv is used')
    parser.add_argument('--reviewers_csv', dest='reviewers_csv',
                        help='path of the reviewers csv, if not provided <data_dir>/reviewers.csv is used')
    parser.add_argument('--no-index', dest='index', help='Don\'t create indices', action='store_false')

    args = parser.parse_args(arguments)

    if args.index:
        print('Creating indices')
        run_script(args.db_url, args.db_name, './program_queries/index.cypher')

    with open(args.script_path, mode='r', encoding='utf8') as script:
        queries = [query.strip() for query in script.read().split('//--')]
        params = {'data_csv': args.data_csv or os.path.join(args.data_dir, 'data.csv'),
                  'citations_csv': args.citations_csv or os.path.join(args.data_dir, 'citations.csv'),
                  'reviewers_csv': args.reviewers_csv or os.path.join(args.data_dir, 'reviewers.csv')}
        named_queries = [(query.splitlines()[0][3:], query, params) for query in queries]
        run_queries(args.db_url, args.db_name, named_queries)


if __name__ == '__main__':
    load_database(sys.argv[1:])
