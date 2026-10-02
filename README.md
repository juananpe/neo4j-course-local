# Neo4j knowledge graph course — local reader

A local reader for Neo4j GraphAcademy’s **Building Knowledge Graphs with LLMs**, with all 11 current lessons, images, PDFs, quiz hints/solutions, exercise code, and a Docker setup for the three-article 1976 election graph.

## Read the course

Requires Python 3. Clone this repository and start the reader:

```sh
git clone https://github.com/juananpe/neo4j-course-local.git
cd neo4j-course-local
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8765. You can also open `site/index.html` directly. Reading works offline after cloning. On macOS/Linux, `./start.sh` starts the same server.

## Explore the election knowledge graph

Requires Docker with Docker Compose and Python 3. Start Docker Desktop first, then run from the repository root:

```sh
python3 neo4j/setup.py
```

This creates a random local password, starts Neo4j 5.26 Community, and imports the course’s exact sample graph: **26 nodes, 47 relationships, three articles**. Setup can be rerun without duplicating the graph.

Open http://127.0.0.1:7474/browser/ and connect to `bolt://127.0.0.1:7687`, username `neo4j`, with the password saved in `neo4j/.env`.

```cypher
MATCH p=(a:Article)-[:HAS_ENTITY]->(e)-[r]-()
RETURN p
```

Data persists in a Docker volume. To stop and restart:

```sh
docker compose -f neo4j/compose.yaml stop
docker compose -f neo4j/compose.yaml up -d
```

Ports 7474 and 7687 must be available. No API key or LLM is needed for this prebuilt graph. More queries are in [neo4j/README.md](neo4j/README.md).

## Files and rebuilding

- `curriculum/`: a snapshot of the official course sources.
- `exercises/`: a snapshot of the official exercise repository.
- `site/`: ready-to-browse HTML and local assets.
- `renderer/`: the reader generator.
- `neo4j/`: Docker configuration and graph import scripts.

To rebuild after editing the course sources, install Node.js 20+ and run:

```sh
npm ci --prefix renderer
node renderer/build.js
```

Hosted sandboxes, external tools, API requests, enrollment and certification require their respective online services. For other hands-on exercises, supply your own credentials. Quiz answer markings from the source are visible, with expandable hints and solutions. Relationships in the sample graph are generated course material; check them against the article text when assessing historical claims.

## Attribution

This is an unofficial teaching mirror. Course content and exercise code originate from Neo4j GraphAcademy; authors retain their respective rights. See [SOURCES.md](SOURCES.md) for upstream URLs and snapshot commits. No new license is asserted over upstream material.
