// Find the database community
MATCH (n:Publication)-[h:has]->(k:Keyword)
WHERE k.keyword IN ["data management", "indexing", "data modeling", "big data", "data processing", "data storage","data querying"]
RETURN *
;

// Find conferences and journals related to the database community
MATCH (p:Publication)-[:published_in]->()-[:belongs_to*0..1]->(c)
  WHERE c:Conference OR c:Journal
WITH c, count(DISTINCT p) as total_papers
MATCH (k:Keyword)<-[:has]-(p_db:Publication)-[:published_in]->(c:Journal)
  WHERE k.keyword IN ["data management", "indexing", "data modeling", "big data", "data processing", "data storage","data querying"]
WITH c, total_papers, count(DISTINCT p_db) as database_community_papers
  WHERE toFloat(database_community_papers)/total_papers > 0.9
RETURN c
;

// Find the papers with the highest page rank of the conferences and journals related to the database community
// Step by step: For each community, get all papers, compute their page rank, return the top papers

// Create projection of papers published in journals/conferences that are in the database community
CALL gds.graph.create.cypher(
  // graph name
  'papers_in_database_communities_journals_or_conferences',
  // node query: return the nodes for publications published in journals/conferences from the database community
  'MATCH (p:Publication)-[:published_in]->()-[:belongs_to*0..1]->(c)
      WHERE c:Conference OR c:Journal
    WITH c, count(DISTINCT p) as total_papers
    MATCH (k:Keyword)<-[:has]-(p_db:Publication)-[:published_in]->(c:Journal)
      WHERE k.keyword IN ["data management", "indexing", "data modeling", "big data", "data processing", "data storage","data querying"]
    WITH c, total_papers, count(DISTINCT p_db) as database_community_papers
      WHERE toFloat(database_community_papers)/total_papers > 0.9
    WITH c
    MATCH (p:Publication)-[:published_in]->()-[:belongs_to*0..1]->(c)
      WHERE c:Conference OR c:Journal
    RETURN id(p) AS id',
  // relationship query
  'MATCH (n:Publication)-[r:cites]->(m:Publication) RETURN id(n) AS source, id(m) AS target',
  {validateRelationships:false}
)
;

// Run the PageRank algorithm in write mode and write the page rank as a property for the papers in journals/conferences given above
CALL gds.pageRank.write('papers_in_database_communities_journals_or_conferences', {
  maxIterations: 20,
  dampingFactor: 0.85,
  writeProperty: 'pagerank'
})
;

// Return the top papers for each community based on their page rank
MATCH (p:Publication)-[:published_in]->()-[:belongs_to*0..1]->(c)
      WHERE c:Conference OR c:Journal
WITH c, count(DISTINCT p) as total_papers
MATCH (k:Keyword)<-[:has]-(p_db:Publication)-[:published_in]->(c:Journal)
  WHERE k.keyword IN ["data management", "indexing", "data modeling", "big data", "data processing", "data storage","data querying"]
WITH c, total_papers, count(DISTINCT p_db) as database_community_papers
  WHERE toFloat(database_community_papers)/total_papers > 0.9
WITH c
MATCH (p:Publication)-[:published_in]->()-[:belongs_to*0..1]->(c)
  WHERE c:Conference OR c:Journal
WITH c, p ORDER BY p.pagerank DESC
WITH c, COLLECT(p) AS p
RETURN c,p[0..2]
ORDER BY c