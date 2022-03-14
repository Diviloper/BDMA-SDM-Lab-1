import csv


def analyze_data(data_csv):
    with open(data_csv, encoding='utf8') as file:
        data = list(csv.reader(file))[1:]
    print(f'=============================================================================')
    print(f'Analyzing data from {data_csv}')
    print(f'=============================================================================')
    print(f'Number of publications: {len(data)}')
    print(f'Number of Titles: {len({paper[2] for paper in data})}')
    print(f'Number of DOIs: {len({paper[12] for paper in data})}')
    print(f'Number of Links: {len({paper[13] for paper in data})}')
    print(f'Number of Authors: {len({author for paper in data for author in paper[1].split(";")}) - 1}')
    print(f'Number of Author-Paper: '
          f'{sum(len(paper[1].split(";")) - (1 if paper[1].endswith(";") else 0) for paper in data)}')
    print(f'Number of Keywords: {len({key.strip() for paper in data for key in paper[18].split(";")})}')
    print(f'Number of Publishers: {len({paper[4] for paper in data})}')
    print(f'Number of Journals: {len({paper[4] for paper in data if paper[19] == "Article"})}')
    print(f'Number of Conferences: {len({paper[4] for paper in data if paper[19] == "Conference Paper"})}')

    author_papers = {}
    for paper in data:
        for author in paper[1].split(';')[:-1]:
            author_papers[author] = author_papers[author] + 1 if author in author_papers else 1
    print(f'Average papers per author: {sum(author_papers.values()) / len(author_papers):.2f}')

    journal_articles = [paper for paper in data if paper[19] == 'Article']
    journals = {paper[4] for paper in journal_articles}
    print(f'Average paper per journal: {len(journal_articles) / len(journals):.2f}')

    conference_papers = [paper for paper in data if paper[19] == 'Conference Paper']
    conferences = {paper[4] for paper in conference_papers}
    print(f'Average paper per conference: {len(conference_papers) / len(conferences):.2f}')

    print(f'=============================================================================')


if __name__ == '__main__':
    analyze_data('./data/csvs/clean_data.csv')
    analyze_data('./data/csvs/expanded_data.csv')
