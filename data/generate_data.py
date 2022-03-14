import csv
import random
import re


def clean_data(data_csv, clean_data_csv):
    with open(data_csv, encoding='utf8') as file, \
            open(clean_data_csv, encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        csv_file = csv.reader(file)
        headers = next(csv_file)
        output.writerow(headers)

        dois = set()
        for row in csv_file:
            # Remove publications that are neither an Article nor a Conference Paper
            if row[19] not in ['Article', 'Conference Paper']:
                continue
            authors = row[0].split(', ')
            affiliations = row[15].split('; ')
            # Remove publications with a mismatch in the author information
            if len(authors) != len(affiliations):
                continue
            # Remove publications without a DOI
            if not row[12]:
                continue
            # Remove duplicated publications
            if row[12] in dois:
                continue
            # Remove publications without keywords
            if not row[18]:
                continue
            dois.add(row[12])

            # Remove edition info (year and edition numnber) from conference names
            values = [r'\d+((st)|(nd)|(rd)|(th)) ', r'\d{4}']
            for reg in values:
                row[4] = re.sub(reg, '', row[4])

            output.writerow(row)


def expand_data(data_csv, expanded_data_csv):
    with open(data_csv, encoding='utf8') as file:
        data = list(csv.reader(file))[1:]


def create_citation_csv(data_csv, citations_csv):
    with open(data_csv, encoding='utf8') as file:
        data = list(csv.reader(file))[1:]

    # Sort papers by year
    data.sort(key=lambda x: int(x[3]))

    # Get the keywords of each paper
    keywords = [set(paper[18].split('; ')) for paper in data]

    citations = []
    for index, paper in enumerate(data):
        # Get the citable papers -> papers published previously with at least one keyword in common
        citable_papers = [(i, p[12]) for i, p in enumerate(data[:index]) if
                          p[3] != paper[3] and not keywords[i].isdisjoint(keywords[index])]

        # If there is no citable paper we just don't cite anything
        if len(citable_papers) == 0:
            continue
        # If there is less than 5 citable papers, we cite them all
        if len(citable_papers) < 10:
            cited_papers = citable_papers
        # Otherwise, we cite a random number of papers between 10 and 20
        else:
            num_citations = min(random.randint(10, 20), len(citable_papers))
            cited_papers = random.sample(citable_papers, num_citations)

        citations.extend([(paper[12], citation[1]) for citation in cited_papers])

    with open(citations_csv, encoding='utf8', mode='w+', newline='') as output_file:
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


def create_review_csv(data_csv, reviews_csv, reviewers_csv):
    with open(data_csv, encoding='utf8') as file:
        data = list(csv.reader(file))[1:]

    # Get the keywords related to an author -> Keywords that are present in at least one of their papers
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
        # Get the potential reviewers of the paper -> People other than the authors of the paper that
        #                                               have some keywords in common with the paper
        potential_reviewers = [author for author, keywords in author_keywords.items() if
                               author not in paper_authors and not keywords.isdisjoint(paper_keywords)]

        # If there is less than 3 potential reviewers, we choose from the whole set of authors
        if len(potential_reviewers) < 3:
            potential_external_reviewers = [author for author in author_keywords if author not in paper_authors]
            paper_reviewers = set(potential_reviewers)
            while len(paper_reviewers) < 3:
                paper_reviewers.add(random.choice(potential_external_reviewers))
            paper_reviewers = list(paper_reviewers)
        # If there are more, we randomly chose 3
        else:
            paper_reviewers = random.sample(potential_reviewers, 3)

        # Save the list of reviewers
        reviewers.append([paper[12], ';'.join(paper_reviewers)])

        # We chose a decision (True = Approved, False = Rejected) for each of them
        # Since all papers in the database must be published and there are 3 reviewers, at most 1 can reject the paper
        decisions = random.sample([True, False], 3, counts=[5, 1])

        for reviewer, decision in zip(paper_reviewers, decisions):
            # Generate a review for the revision
            review = generate_review(decision)
            reviews.append([paper[12], reviewer, decision, review])

    with open(reviews_csv, encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Paper', 'Reviewer', 'Decision', 'Review'])
        output.writerows(reviews)
    with open(reviewers_csv, encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Paper', 'Reviewers'])
        output.writerows(reviewers)


def extract_affiliations(data_csv, affiliations_csv):
    with open(data_csv, encoding='utf8') as file:
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
    with open(affiliations_csv, encoding='utf8', mode='w+', newline='') as output_file:
        output = csv.writer(output_file)
        output.writerow(['Author', 'Organization Name', 'Type'])
        output.writerows(flat_affiliations)


if __name__ == '__main__':
    clean_data(data_csv='./data/csvs/data.csv', clean_data_csv='./data/csvs/clean_data.csv')
    # expand_data(data_csv='./data/csvs/clean_data.csv', expanded_data_csv='./data/csvs/expanded_data.csv')
    # create_citation_csv(data_csv='./data/csvs/expanded_data.csv', citations_csv='./data/csvs/citations.csv')
    # create_review_csv(data_csv='./data/csvs/expanded_data.csv', reviews_csv='./data/csvs/reviews.csv',
    #                   reviewers_csv='./data/csvs/reviewers.csv')
    # extract_affiliations(data_csv='./data/csvs/expanded_data.csv', affiliations_csv='./data/csvs/affiliations.csv')
