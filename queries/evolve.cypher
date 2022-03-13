// Load affiliations

LOAD CSV WITH HEADERS FROM 'file:///affiliations.csv' AS line
MERGE (o :Organization {name: line.`Organization Name`, type: line.Type})
WITH line, o
MATCH (a :Author {id: line.Author})
CREATE (a) -[:affiliated_to]-> (o)

// Add proper labels to organizations
MATCH (o :Organization {type: 'University'})
SET o:University
REMOVE o.type

MATCH (o :Organization {type: 'Company'})
SET o:Company
REMOVE o.type


// Load Review info
LOAD CSV WITH HEADERS FROM 'file:///reviews.csv' AS line
MATCH (:Publication {title: line.Paper}) <-[r:reviews]- (:Author {id: line.Reviewer})
SET
  r.Decision = line.Decision,
  r.Review = line.Review