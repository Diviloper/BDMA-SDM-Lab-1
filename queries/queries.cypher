// Query 3 Impact factor
// For every year
MATCH (journal:Journal)<-[:published_in]-(p:Publication) <-[c:cites]-(:Publication)
WITH journal, p.year AS year, count(c) AS citations
MATCH (journal)<-[:published_in]-(p:Publication)
  WHERE p.year = year - 1 OR p.year = year - 2
WITH journal, year, citations, count(p) AS publications
  WHERE publications > 0
RETURN journal, year, citations, publications, toFloat(citations) / publications AS ImpactFactor
  ORDER BY ImpactFactor DESC

// For a single year
MATCH (journal:Journal)<-[:published_in]-(p:Publication {year: 2019}) <-[c:cites]-(:Publication)
WITH journal, p.year AS year, count(c) AS citations
MATCH (journal)<-[:published_in]-(p:Publication)
  WHERE p.year = year - 1 OR p.year = year - 2
WITH journal, year, citations, count(p) AS publications
  WHERE publications > 0
RETURN journal, year, citations, publications, toFloat(citations) / publications AS ImpactFactor
  ORDER BY ImpactFactor DESC


// Query 4 H-Index
MATCH (author:Author)-[:writes]->(paper:Publication) <-[c:cites]-(:Publication)
WITH author, paper, count(c) AS citations
  ORDER BY author, citations DESC
WITH author, collect(citations) AS paper_citations
RETURN author,
       reduce(hindex = 0,
       citations IN paper_citations |
       CASE WHEN citations > hindex THEN hindex + 1
         ELSE hindex
         END) AS `H-Index`
;
//reduce(lambda h_index, next_citations: h_index + 1 if next_citations >= h_index else h_index, cites, 0)