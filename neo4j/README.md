# 1976 election course graph

Initial setup: `python3 neo4j/setup.py` from the repository root.

Start again: `docker compose up -d` from this directory.

Import or verify: `python3 load_graph.py` (safe to rerun).

Browse: http://127.0.0.1:7474/browser/

Connect to `bolt://127.0.0.1:7687`, username `neo4j`. Password is in the local `.env` file.

Explore the graph:

```cypher
MATCH p=(a:Article)-[:HAS_ENTITY]->(e)-[r]-()
RETURN p
```

Explore Jimmy Carter:

```cypher
MATCH (p:Person {id:"Jimmy Carter"})-[r]-(p2:Person)
RETURN p, r, p2
```

Read the articles:

```cypher
MATCH (a:Article) RETURN a.id, a.date, a.text ORDER BY a.id
```

Stop: `docker compose stop`. Start again: `docker compose up -d`.

Data persists in the Docker volume `graphacademy-election_election-data`.
The server binds only to localhost. It uses Neo4j 5.26 Community and the exact official course JSON; no LLM calls or APOC plugin are required.

Source: ../curriculum/asciidoc/courses/llm-knowledge-graph-construction/modules/1-knowledge-graphs/lessons/3-explore/data/jimmy_carter.json

The relationships come from the course's generated graph and should be evaluated against the article text rather than treated as verified historical facts.
