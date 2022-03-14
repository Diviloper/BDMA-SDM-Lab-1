CREATE INDEX publication_index
FOR (n:Publication)
ON (n.doi)
;

CREATE INDEX author_index
FOR (n:Author)
ON (n.id)
;

CREATE INDEX keyword_index
FOR (n:Keyword)
ON (n.keyword)
;