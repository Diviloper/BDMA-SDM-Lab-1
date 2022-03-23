CREATE INDEX publication_index_ZD
FOR (n:Publication)
ON (n.doi)
;
//--
CREATE INDEX author_index_ZD
FOR (n:Author)
ON (n.id)
;
//--
CREATE INDEX keyword_index_ZD
FOR (n:Keyword)
ON (n.keyword)
;