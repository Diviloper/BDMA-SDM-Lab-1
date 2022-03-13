import csv


def analyze_data():
    with open('./data/csvs/clean_data.csv', encoding='utf8') as file:
        data = list(csv.reader(file))[1:]
    print(f'Number of publications: {len(data)}')
    print(f'Number of Titles: {len({paper[2] for paper in data})}')
    print(f'Number of DOIs: {len({paper[12] for paper in data})}')
    print(f'Number of Links: {len({paper[13] for paper in data})}')
    print(f'Number of Authors: {len({author for paper in data for author in paper[1].split(";")}) - 1}')
    print(f'Number of Author-Paper: '
          f'{sum(len(paper[1].split(";")) - (1 if paper[1].endswith(";") else 0) for paper in data)}')
    print(f'Number of Keywords: {len({key.strip() for paper in data for key in paper[18].split(";")})}')
    print(f'Number of Publishers: {len({paper[4] for paper in data})}')

    author_papers = {}
    for paper in data:
        for author in paper[1].split(';')[:-1]:
            author_papers[author] = author_papers[author] + 1 if author in author_papers else 1
    print(f'Average papers per author: {sum(author_papers.values()) / len(author_papers)}')


if __name__ == '__main__':
    analyze_data()
