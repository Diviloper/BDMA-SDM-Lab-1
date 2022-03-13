import csv
import random


def clean_data():
    with open('./data/data.csv', encoding='utf8') as file, \
            open('./data/clean_data.csv', encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        csv_file = csv.reader(file)
        headers = next(csv_file)
        output.writerow(headers)
        for row in csv_file:
            if row[19] not in ['Article', 'Conference Paper']:
                continue
            authors = row[0].split(', ')
            affiliations = row[15].split('; ')
            if len(authors) != len(affiliations):
                continue
            output.writerow(row)


def create_citation_csv():
    with open('./data/clean_data.csv', encoding='utf8') as file:
        data = list(csv.reader(file))[1:]
    data.sort(key=lambda x: int(x[3]))
    keywords = [set(paper[18].split('; ')) for paper in data]
    citations = []
    for index, paper in enumerate(data):
        citable_papers = [(i, p[2]) for i, p in enumerate(data[:index]) if
                          p[3] != paper[3] and not keywords[i].isdisjoint(keywords[index])]
        if len(citable_papers) == 0:
            continue
        if len(citable_papers) < 5:
            citations.extend([(paper[2], citation[1]) for citation in citable_papers])
        else:
            num_citations = min(random.randint(10, 20), len(citable_papers))
            cited_papers = random.sample(citable_papers, num_citations)
            citations.extend([(paper[2], citation[1]) for citation in cited_papers])

    with open('./data/citations.csv', encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Paper', 'Citation'])
        output.writerows(citations)


def generate_review(decision):
    return random.choice([
                             'The best thing I have ever read',
                             'Interesting',
                             'Not bad at all',
                         ] if decision else [
        'I would not even use it as toilet paper',
        'My dog can write better',
        'Meh',
        'I fell asleep while reading',
        'Nothing makes sense',
        'Is this a joke?'
    ])


def create_review_csv():
    with open('./data/clean_data.csv', encoding='utf8') as file:
        data = list(csv.reader(file))[1:]
    author_keywords = {}
    for paper in data:
        authors = paper[1].split(';')
        keywords = set(paper[18].split('; '))
        for author in authors:
            if author in author_keywords:
                author_keywords[author].update(keywords)
            else:
                author_keywords[author] = keywords
    reviews = []
    reviewers = []
    for paper in data:
        paper_authors = paper[1].split(';')
        paper_keywords = set(paper[18].split('; '))
        potential_reviewers = [author for author, keywords in author_keywords.items() if
                               author not in paper_authors and not keywords.isdisjoint(paper_keywords)]
        if len(potential_reviewers) < 3:
            paper_reviewers = random.sample([author for author in author_keywords if author not in paper_authors], 3)
        else:
            paper_reviewers = random.sample(potential_reviewers, 3)
        reviewers.append([paper[2], ';'.join(paper_reviewers)])
        decisions = random.sample([True, False], 3, counts=[5, 1])
        for reviewer, decision in zip(paper_reviewers, decisions):
            review = generate_review(decision)
            reviews.append([paper[2], reviewer, decision, review])

    with open('./data/reviews.csv', encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Paper', 'Reviewer', 'Decision', 'Review'])
        output.writerows(reviews)
    with open('./data/reviewers.csv', encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Paper', 'Reviewers'])
        output.writerows(reviewers)


def extract_affiliations():
    with open('./data/clean_data.csv', encoding='utf8') as file:
        data = list(csv.reader(file))[1:]
    affiliations = {}
    for paper in data:
        auth_ids = {name: auth_id for name, auth_id in zip(paper[0].split(', '), paper[1].split(';'))}
        author_affiliations = paper[15].split('; ')
        for affiliation in author_affiliations:
            parts = affiliation.split(', ')
            if len(parts) < 3:
                continue
            name = f'{parts[0]} {parts[1]}'
            author_id = auth_ids[name]
            uni = next(
                (i for i in parts[2:] if any((x in i.lower() for x in ['univ', 'college', 'institut', 'academ']))),
                None)
            org = (uni or parts[2], 'University' if uni else 'Company')
            if author_id in affiliations:
                affiliations[author_id].add(org)
            else:
                affiliations[author_id] = {org}
    flat_affiliations = [
        [author, org, org_type]
        for author, aff in affiliations.items()
        for org, org_type in aff
    ]
    with open('./data/affiliations.csv', encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Author', 'Organization Name', 'Type'])
        output.writerows(flat_affiliations)


if __name__ == '__main__':
    # clean_data()
    # create_citation_csv()
    # create_review_csv()
    extract_affiliations()
