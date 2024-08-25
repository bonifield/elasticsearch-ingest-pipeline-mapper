#!/usr/bin/env python3

#===========================
#
# this script attempts to visually diagram your Elasticsearch ingest pipelines
# additional filtering, such as ignoring anything beyond synthetics, metrics and traces, is up to you
#
# installation
#     sudo apt-get install graphviz graphviz-dev
#     python3 -m pip install pygraphviz
#
# usage
#     python3 pipeline-mapper.py
#
# view image
#     eog /tmp/dot.png
#
#===========================

import argparse
import json
# suppress InsecureRequestWarning from urllib3 if using verify=False to access websites using self-signed certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
#
import requests
import pygraphviz as pgv

# command line arguments
parser = argparse.ArgumentParser(description="visually diagram Elasticsearch ingest pipelines")
# add optional arguments
parser.add_argument("-u", "--username", dest="user", default="elastic", type=str, help="your Elasticsearch username")
parser.add_argument("-p", "--password", dest="password", default="abcd1234", type=str, help="your Elasticsearch password")
parser.add_argument("-s", "--server", dest="server", default="https://elasticsearch.local:9200/_ingest/pipeline", type=str, help="your Elasticsearch URL")
parser.add_argument("-d", "--dotfile", dest="dotfile", default="/tmp/graph.dot", type=str, help="dot text file output path")
parser.add_argument("-o", "--outfile", dest="outfile", default="/tmp/dot.png", type=str, help="dot image output path")
args = vars(parser.parse_args())
user = args["user"]
password = args["password"]
server = args["server"]
dotfile = args["dotfile"]
outfile = args["outfile"]

response = requests.get(server, verify=False, auth=(user, password))
j = json.loads(response.text)

# create graph object, digraph (strict=False), force-directed, rank left-to-right
G = pgv.AGraph(strict=False, directed=True, rankdir="LR")

# all keys are pipeline names
for pipeline,v in j.items():
	if not re.findall("synthetics|metrics|traces", pipeline, re.I|re.DOTALL):
		# key string cleanup
		pipeline = pipeline.replace("{","").replace("}","").replace('"',"").replace("'","").strip().replace(" ","_")
		# each pipeline's value is a list of subprocessors
		for proc in v["processors"]:
			# pipelines with subprocessors leading to another pipeline
			if "pipeline" in proc:
				# more key string cleanup
				next_pipeline = proc["pipeline"]["name"].replace("{","").replace("}","").replace('"',"").replace("'","").strip().replace(" ","_")
				#print(f'"{pipeline}" -> "{next_pipeline}"')
				# add_edge adds both edges and nodes at the same time
				G.add_edge(pipeline, next_pipeline)

#print(G)

# write dot file
G.write(f"{dotfile}")
# draw image
G.draw(f"{outfile}", prog="dot")
