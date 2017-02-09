mapping = {
    "settings": {
        "index": {
            "max_result_window": 15000,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": ["english_stemmer", "lowercase"]
                    },
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": ["lowercase", "autocomplete_filter"]
                    },
                    "symbols": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": ["lowercase"]
                    }
                },
                "filter": {
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": "1",
                        "max_gram": "20"
                    }
                }
            },
            "number_of_replicas": "0", #temporarily
            "number_of_shards": "5"
        }
    },
    "mappings": {
        "searchable_item": {
            "properties": {
                "name": {
                    "type": "string",
                    "fields": {
                        "symbol": {
                            "type": "string",
                            "analyzer": "symbols"
                        }
                    }
                },
                "gene_symbol": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "gene_synonyms": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "gene_type": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_chromosomes": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_chromosome_starts": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_chromosome_ends": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_chromosome_strand": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "description": {
                    "type": "string"
                },
                "external_ids": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "gene_biological_process": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "symbol": {
                            "type": "string",
                            "analyzer": "symbols"
                        }

                    }
                },
                "gene_molecular_function": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "symbol": {
                            "type": "string",
                            "analyzer": "symbols"
                        }

                    }
                },
                "gene_cellular_component": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "symbol": {
                            "type": "string",
                            "analyzer": "symbols"
                        }

                    }
                },
                "species": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "href": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "category": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "go_type": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "go_genes": {
                    "type": "string",
                    "analyzer": "symbols",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "go_species": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "disease_genes": {
                    "type": "string",
                    "analyzer": "symbols",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "disease_species": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "disease_synonyms": {
                    "type": "string"
                },
                "id": {
                    "type": "string",
                    "analyzer": "symbols"
                },
                "name_key": {
                    "type": "string",
                    "analyzer": "symbols",
                    "fields": {
                        "autocomplete": {
                            "type": "string",
                            "analyzer": "autocomplete"
                        }
                    }
                },
                "homologs": {
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "analyzer": "symbols"
                        },
                        "species": {
                            "type": "string"
                        },
                        "relationship_type": {
                            "type": "string"
                        },
                        "ancestral": {
                            "type": "string"
                        },
                        "panther_family": {
                            "type": "string",
                            "analyzer": "symbols"
                        },
                        "href": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}
