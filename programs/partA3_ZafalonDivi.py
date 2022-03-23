import argparse
import os.path
import sys
from typing import List

from programs.neo4j_helpers import run_queries


def evolve_database(arguments: List[str]):
    parser = argparse.ArgumentParser(description='Evolves the database')
    parser.add_argument('-d', '--db', dest='db_url', help='url of the database (default: "bolt://localhost:7687")',
                        default='bolt://localhost:7687')
    parser.add_argument('-n', '--db_name', dest='db_name',
                        help='name of the database, if not provided the default database will be used')
    parser.add_argument('-s', '--script', dest='script_path',
                        help='path of the query script (default: "./program_queries/evolve.cypher")',
                        default='./program_queries/evolve.cypher')
    parser.add_argument('-f', '--data_dir', dest='data_dir',
                        help='path of the directory containing data (data, citations and reviewers) csvs. This path'
                             'must be relative to Neo4j import files folder (default: "program_csvs")',
                        default='program_csvs')
    parser.add_argument('--affiliations_csv', dest='affiliations_csv',
                        help='path of the affiliations csv, if not provided <data_dir>/affiliations.csv is used')
    parser.add_argument('--reviews_csv', dest='reviews_csv',
                        help='path of the reviews csv, if not provided <data_dir>/reviews.csv is used')

    args = parser.parse_args(arguments)

    with open(args.script_path, mode='r', encoding='utf8') as script:
        queries = [query.strip() for query in script.read().split('//--')]
        params = {'affiliations_csv': args.affiliations_csv or os.path.join(args.data_dir, 'affiliations.csv'),
                  'reviews_csv': args.reviews_csv or os.path.join(args.data_dir, 'reviews.csv')}
        named_queries = [(query.splitlines()[0][3:], query, params) for query in queries]
        run_queries(args.db_url, args.db_name, named_queries)


if __name__ == '__main__':
    evolve_database(sys.argv[1:])
