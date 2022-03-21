// Create Publications and authors
LOAD CSV WITH HEADERS FROM 'file://' + $data_csv AS line
CREATE(p:Publication {
  title:    line.Title,
  year:     toInteger(line.Year),
  doi:      line.DOI,
  link:     line.Link,
  abstract: line.Abstract
})
WITH p, line,
     split(line.Authors, ', ') AS author_names,
     split(line.`Author(s) ID`, ';') AS author_ids
MERGE (a:Author {id: author_ids[0]})
  ON CREATE SET a.name = author_names[0]
CREATE (p)-[:has_corresponding_author]->(a)
CREATE (a)-[:writes]->(p)
WITH p, line, author_names, author_ids, range(1, size(author_names) - 1) AS author_index
UNWIND author_index AS a_index
MERGE (a:Author {id: author_ids[a_index]})
  ON CREATE SET a.name = author_names[a_index]
CREATE (a)-[:writes]->(p)
;
//--
// Create keywords
LOAD CSV WITH HEADERS FROM 'file://' + $data_csv AS line
MATCH (p:Publication {doi: line.DOI})
WITH p, line, split(line.`Index Keywords`, '; ') AS keywords_list
UNWIND keywords_list AS keyword_item
MERGE (k:Keyword {keyword: keyword_item})
CREATE (p)-[:has]->(k)
;
//--
// Create Journals
LOAD CSV WITH HEADERS FROM 'file://' + $data_csv AS line
WITH line
  WHERE line.`Document Type` = 'Article'
MATCH (p:Publication {doi: line.DOI})
MERGE (j:Journal {name: line.`Source title`})
CREATE (p)-[:published_in {volume: coalesce(line.Volume, 0)}]->(j)
;
//--
// Create Conferences
LOAD CSV WITH HEADERS FROM 'file://' + $data_csv AS line
WITH line
  WHERE line.`Document Type` = 'Conference Paper'
MATCH (p:Publication {doi: line.DOI})
MERGE (c:Conference {name: line.`Source title`})
MERGE (ce:ConferenceEdition {year: toInteger(line.Year)})-[:belongs_to]->(c)
CREATE (p)-[:published_in {volume: coalesce(line.Volume, 0)}]->(ce)
;
//--
// Add reviewers
LOAD CSV WITH HEADERS FROM 'file://' + $reviewers_csv AS line
MATCH (p:Publication {doi: line.Paper})
WITH p, split(line.Reviewers, ';') AS reviewers
UNWIND reviewers AS reviewer
MATCH (r:Author {id: reviewer})
CREATE (r)-[:reviews]->(p)
;
//--
// Add citations
LOAD CSV WITH HEADERS FROM 'file://' + $citations_csv AS line
MATCH (p:Publication {doi: line.Paper})
WITH line, p
MATCH (c:Publication {doi: line.Citation})
CREATE (p)-[:cites]->(c)
;