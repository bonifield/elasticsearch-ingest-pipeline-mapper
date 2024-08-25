# Elasticsearch Ingest Pipeline Mapper
Visually diagrams Elasticsearch ingest pipelines using Python and Graphviz

Uses basic authentication (username and password) to request the `_ingest/pipeline` Elasticsearch endpoint

## Usage

Defaults to creating `/tmp/graph.dot` (text dotfile) and `/tmp/dot.png` (graph image)

```
python3 pipeline-mapper.py
```

## Example Output

graph

![example](https://github.com/bonifield/elasticsearch-ingest-pipeline-mapper/blob/main/example.PNG)

dotfile
```
digraph "" {
        graph [rankdir=LR];
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-cassandra";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-dhcpv4";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-dns";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-flow";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-http";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-icmp";
        "packetbeat-8.14.3-routing" -> "packetbeat-8.14.3-memcached";
	...
```

## Prerequisites

```
sudo apt-get install graphviz graphviz-dev
python3 -m pip install pygraphviz
```

## Default Values

If no arguments are given, the following are default values:

- `-u, --user`: `elastic`
- `-p, --password`: `abcd1234`
- `-s, --server`: `https://elasticsearch.local:9200/_ingest/pipeline`
- `-d, --dotfile`: `/tmp/graph.dot`
- `-o, --outfile`: `/tmp/dot.png`
