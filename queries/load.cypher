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
MERGE (a)-[:writes]->(p);


RETURN line.Title, author_ids[a_index], author_names[a_index];