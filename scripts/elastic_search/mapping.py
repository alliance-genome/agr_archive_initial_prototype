mapping = {
    "settings": {
        "index": {
            "max_result_window": 15000,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "standard",
                        "filter": ["english_stemmer", "lowercase"]
                    },
                    'simple': {
                        "type": "standard",
                        "filter": ["lowercase"]
                    },
                    "fulltext": {
                        "tokenizer": "standard",
                        "filter": ["standard", "english_stemmer", "word_split", "lowercase"]
                    },
                    "autocomplete": {
                        "type": "custom",
                        "filter": ["lowercase", "autocomplete_filter"],
                        "tokenizer": "standard"
                    },
                    "raw": {
                        "type": "custom",
                        "filter": ["lowercase"],
                        "tokenizer": "keyword"
                    }
                },
                "filter": {
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "autocomplete_filter": {
                        "min_gram": "1",
                        "type": "edge_ngram",
                        "max_gram": "20"
                    },
                    "word_split": {
                        "type": "word_delimiter",
                        "split_on_numerics": "false"
                    }
                }
            },
            "number_of_replicas": "1",
            "number_of_shards": "5"
        }
    },
    "mappings": {
        "searchable_item": {
            "properties": {
                "name": {
                    "type": "string",
                    "analyzer": "fulltext",
                    "fields": {
                        "simple": {
                            "type": "string",
                            "analyzer": "simple"
                        },
                        "raw": {
                            "type": "string",
                            "analyzer": "raw"
                        },
                        "autocomplete": {
                            "type": "string",
                            "analyzer": "autocomplete"
                        }
                    }
                },
                "symbol": {
                    "type": "string",
                    "fields": {
                        "simple": {
                            "type": "string",
                            "analyzer": "simple"
                        },
                        "raw": {
                            "type": "string",
                            "analyzer": "raw"
                        },
                        "autocomplete": {
                            "type": "string",
                            "analyzer": "autocomplete"
                        }
                    }
                },
                "go_names": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "go_ids": {
                    "type": "string"
                },
                "type": {
                    "type": "string"
                },
                "href": {
                    "type": "string"
                },
                "synonym": {
                    "type": "string"
                }
            }
        }
    }
}
