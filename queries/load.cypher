
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS line
CREATE(p:Publication {
  name: line.Title,
  year: toInteger(line.Year),
  doi: line.DOI,
  link: line.Link,
  abstract: line.Abstract
})
WITH p, line,
     split(line.Authors, ', ') AS author_names,
     split(line.`Author(s) ID`, ';') AS author_ids
WITH p, line, author_names, author_ids, range(0, size(author_names) - 1) AS author_index
UNWIND author_index AS a_index
MERGE (a:Author {id: author_ids[a_index], name: author_names[a_index]})
MERGE (a)-[:writes]->(p)
WITH p, line,
     split(line.`Index Keywords`, '; ') AS keywords_list
UNWIND keywords_list AS keyword_item
MERGE (k:Keyword {keyword: keyword_item})
MERGE (p)-[:has]->(k)
MERGE (j:JournalConference {
  name: line.`Source title`,
  type: line.`Document Type`,
  year: toInteger(line.Year),
  volume: coalesce(line.Volume, 0)})
MERGE (p)-[:published_in]->(j)
;

//TODO: change volume from JournalConference to a property of the relation published_in for Journals
MATCH (j:JournalConference {type:'Article'})
REMOVE j:JournalConference
REMOVE j.year
SET j:Journal
;

MATCH (c:JournalConference {type:'Conference Paper'})
REMOVE c:JournalConference
REMOVE c.volume
SET c:ConferenceEdition
;

MATCH (ce:ConferenceEdition)
MERGE (ce)-[:belongs_to]->(c:Conference {name:ce.name})
;


RETURN line.Title, author_ids[a_index], author_names[a_index];