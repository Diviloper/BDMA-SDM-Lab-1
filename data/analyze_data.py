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


if __name__ == '__main__':
    analyze_data()
