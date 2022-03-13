LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
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
WITH p, line, split(line.`Index Keywords`, '; ') AS keywords_list
UNWIND keywords_list AS keyword_item
MERGE (k:Keyword {keyword: keyword_item})
CREATE (p)-[:has]->(k)
MERGE (j:JournalConference {
  name:   line.`Source title`,
  type:   line.`Document Type`,
  year:   toInteger(line.Year),
  volume: coalesce(line.Volume, 0)})
CREATE (p)-[:published_in]->(j)
;

// Create Publications and authors
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
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

// Create keywords
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
MATCH (p:Publication {doi: line.DOI})
WITH p, line, split(line.`Index Keywords`, '; ') AS keywords_list
UNWIND keywords_list AS keyword_item
MERGE (k:Keyword {keyword: keyword_item})
CREATE (p)-[:has]->(k)
;

// Create Journals
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
MATCH (p:Publication {doi: line.DOI})
MERGE (j:JournalConference {
  name:   line.`Source title`,
  type:   line.`Document Type`,
  year:   toInteger(line.Year),
  volume: coalesce(line.Volume, 0)})
CREATE (p)-[:published_in]->(j)
;

// Add reviewers
LOAD CSV WITH HEADERS FROM 'file:///reviewers.csv' AS line
MATCH (p:Publication {doi: line.Paper})
WITH p, split(line.Reviewers, ';') AS reviewers
UNWIND reviewers AS reviewer
MATCH (r:Author {id: reviewer})
CREATE (r)-[:reviews]->(p)
;

// Add citations
LOAD CSV WITH HEADERS FROM 'file:///citations.csv' AS line
MATCH (p:Publication {doi: line.Paper})
WITH line, p
MATCH (c:Publication {doi: line.Citation})
CREATE (p)-[:cites]->(c)
;

//TODO: change volume from JournalConference to a property of the relation published_in for Journals
MATCH (j:JournalConference {type: 'Article'})
REMOVE j:JournalConference
REMOVE j.year
SET j:Journal
;

MATCH (c:JournalConference {type: 'Conference Paper'})
REMOVE c:JournalConference
REMOVE c.volume
SET c:ConferenceEdition
;

MATCH (ce:ConferenceEdition)
MERGE (c:Conference {name: ce.name})
MERGE (ce)-[:belongs_to]->(c)
;

// Checker query
MATCH (a:Author)
WITH count(a) AS authors
MATCH (p:Publication)
WITH authors, count(p) AS publications
MATCH w = ()-[:writes]->()
WITH authors, publications, count(w) AS writes
MATCH (k:Keyword)
WITH authors, publications, writes, count(k) AS keywords
RETURN authors, publications, writes, keywords