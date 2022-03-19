// Create a graph using a native projection and store it in the graph catalog under the name 'publications'.
CALL gds.graph.create(
  'publications',
  'Publication',
  'cites'
)

// Estimate the memory requirements for running the algorithm
CALL gds.pageRank.write.estimate('publications', {
  writeProperty: 'pageRank',
  maxIterations: 20,
  dampingFactor: 0.85
})
YIELD nodeCount, relationshipCount, bytesMin, bytesMax, requiredMemory

// Run the PageRank algorithm in stream mode
CALL gds.pageRank.stream('publications')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).title AS title, score
ORDER BY score DESC, title ASC

// Run the Louvain algorithm in stram mode
CALL gds.louvain.stream('publications')
YIELD nodeId, communityId, intermediateCommunityIds
RETURN gds.util.asNode(nodeId).title AS title, communityId, intermediateCommunityIds
ORDER BY title ASC