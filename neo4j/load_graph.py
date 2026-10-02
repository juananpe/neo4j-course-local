#!/usr/bin/env python3
"""Import the exact course graph with parameterized Cypher; safe to rerun."""
import base64,json,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parent
password=dict(line.split('=',1) for line in (ROOT/'.env').read_text().splitlines() if '=' in line)['NEO4J_PASSWORD']
source=ROOT.parent/'curriculum/asciidoc/courses/llm-knowledge-graph-construction/modules/1-knowledge-graphs/lessons/3-explore/data/jimmy_carter.json'
records=[json.loads(line) for line in source.read_text().splitlines()]
def query(statements):
 req=urllib.request.Request('http://127.0.0.1:7474/db/neo4j/tx/commit',data=json.dumps({'statements':statements}).encode(),headers={'Content-Type':'application/json','Authorization':'Basic '+base64.b64encode(('neo4j:'+password).encode()).decode()})
 with urllib.request.urlopen(req,timeout=30) as response:result=json.load(response)
 if result['errors']:raise RuntimeError(result['errors'])
 return result['results']
def stmt(s,**p):return {'statement':s,'parameters':p}
def ident(s):return '`'+s.replace('`','``')+'`'
for attempt in range(60):
 try:query([stmt('RETURN 1')]);break
 except (urllib.error.URLError,RuntimeError,TimeoutError):time.sleep(2)
else:raise RuntimeError('Neo4j did not become ready within 120 seconds')
labels=sorted({l for r in records if r['type']=='node' for l in r['labels']})
query([stmt(f'CREATE CONSTRAINT {ident("course_"+str(i))} IF NOT EXISTS FOR (n:{ident(label)}) REQUIRE n.neo4jImportId IS UNIQUE') for i,label in enumerate(labels)])
statements=[]
for r in records:
 if r['type']=='node':
  label=':'.join(ident(l) for l in r['labels'])
  statements.append(stmt(f'MERGE (n:{label} {{neo4jImportId:$key}}) SET n += $props',key=r['id'],props=r.get('properties',{})))
for r in records:
 if r['type']=='relationship':
  a=ident(r['start']['labels'][0]);b=ident(r['end']['labels'][0]);rel=ident(r['label'])
  statements.append(stmt(f'MATCH (a:{a} {{neo4jImportId:$start}}), (b:{b} {{neo4jImportId:$end}}) MERGE (a)-[r:{rel} {{neo4jImportId:$key}}]->(b) SET r += $props',start=r['start']['id'],end=r['end']['id'],key=r['id'],props=r.get('properties',{})))
query(statements)
results=query([stmt('MATCH (n) RETURN count(n)'),stmt('MATCH ()-[r]->() RETURN count(r)'),stmt('MATCH (a:Article) RETURN a.id ORDER BY a.id'),stmt('MATCH (a:Article)-[:HAS_ENTITY]->(:Person {id:"Jimmy Carter"}) RETURN a.id ORDER BY a.id')])
counts=[x['data'] for x in results]
assert counts[0][0]['row']==[26] and counts[1][0]['row']==[47],counts
assert {x['row'][0] for x in counts[2]}=={'1976-6','1976-8','1976-22'},counts
assert len(counts[3])==3,counts
print('Verified: 26 nodes, 47 relationships, 3 articles, all connected to Jimmy Carter.')
