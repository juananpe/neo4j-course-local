#!/usr/bin/env python3
"""Generate local credentials, start Neo4j, and import the election graph."""
from pathlib import Path
import secrets,subprocess,sys
root=Path(__file__).resolve().parent
credentials=root/'.env'
if not credentials.exists():
    credentials.write_text('NEO4J_PASSWORD='+secrets.token_urlsafe(18)+'\n')
    credentials.chmod(0o600)
subprocess.run(['docker','compose','up','-d'],cwd=root,check=True)
subprocess.run([sys.executable,str(root/'load_graph.py')],check=True)
print('Open http://127.0.0.1:7474/browser/ — username neo4j; password in .env')
