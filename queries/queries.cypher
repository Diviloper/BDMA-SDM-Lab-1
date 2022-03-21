// Query 1 Top 3 most cited authors per conference
MATCH(:Publication)-[r:cites]->(cited_paper:Publication)-[:published_in]->(:ConferenceEdition)
       -[:belongs_to]->(conf:Conference)
WITH conf, cited_paper, count(r) AS num_citations
  ORDER BY conf, num_citations DESC
WITH conf, collect(cited_paper)[..3] AS top3_most_cited_papers
RETURN conf,
       top3_most_cited_papers[0] AS top1_paper,
       top3_most_cited_papers[1] AS top2_paper,
       top3_most_cited_papers[2] AS top3_paper
;

//Query 2 Authors that have published in the same conference in at least 4 editions
MATCH (a:Author)-[:writes]->(p:Publication)-[:published_in]->(ce:ConferenceEdition)-[:belongs_to]->(c:Conference)
WITH c, a, count(DISTINCT ce) AS distinct_editions
  WHERE distinct_editions >= 4
RETURN c, a
;

// Query 3 Impact factor
// For every year
MATCH (journal:Journal)<-[:published_in]-(p:Publication)<-[c:cites]-(:Publication)
WITH journal, p.year AS year, count(c) AS citations
MATCH (journal)<-[:published_in]-(p:Publication)
  WHERE p.year = year - 1 OR p.year = year - 2
WITH journal, year, citations, count(p) AS publications
  WHERE publications > 0
RETURN journal, year, toFloat(citations) / publications AS ImpactFactor
  ORDER BY ImpactFactor DESC

// For a single year
MATCH (journal:Journal)<-[:published_in]-(p:Publication {year: 2019})<-[c:cites]-(:Publication)
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
//reduce(lambda h_index, next_citations: h_index + 1 if next_citations > h_index else h_index, cites, 0)