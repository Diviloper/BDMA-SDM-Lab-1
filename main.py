from neo4j import GraphDatabase


def main():
    driver = GraphDatabase.driver('bolt://localhost:7687')
    session = driver.session()
    result = session.run('MATCH (n) RETURN n')
    value = result.values()
    print(value[0])
    session.close()


if __name__ == '__main__':
    main()
