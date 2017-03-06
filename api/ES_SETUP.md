# Install and start a local instance of [elasticsearch][1]

## Download tar.gz ES package, 5 or higher.
Save into your favorite location for downloading files, the file format should be something like: elasticsearch-5.x.x.tar.gz

## Install ES

```bash
    a) > cd to your favorite location where you downloaded ES elasticsearch-5.x.x.tar.gz
    b) > tar -xvf elasticsearch-5.x.x.tar.gz
```
## Start your local ES

```bash
    a) > cd elasticsearch-5.x.x/
    b) elasticsearch-5.x.x> ./bin/elasticsearch
    c) Check that ES is running - check http:://localhost:9200/ in a web browser
	    Output should look something like the following:
		{
			"name" : "eOuYijl",
			"cluster_name" : "elasticsearch",
			"cluster_uuid" : "UhmuYCDXTDWTNS-aBrSixQ",
			"version" : {
				"number" : "5.2.1",
				"build_hash" : "db0d481",
				"build_date" : "2017-02-09T22:05:32.386Z",
				"build_snapshot" : false,
				"lucene_version" : "6.4.1"
			},
			"tagline" : "You Know, for Search"
		}
    d) Watch the ES console for errors 
    e) Hit CTRL-C to stop the running server.
``` 

## Runnig the Indexer
In order to get data into this Local elasticsearch instance you will need to run the indexer: See [running the indexer][2] for more info.

[1]: https://www.elastic.co/downloads/elasticsearch
[2]: https://github.com/alliance-genome/agr_indexer
