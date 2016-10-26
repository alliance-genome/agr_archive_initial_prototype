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
            "number_of_replicas": "0", #temporarily
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
                "gene_symbol": {
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
                "gene_synonyms": {
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
                "external_ids": {
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
                "gene_biological_process": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_molecular_function": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "gene_cellular_component": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
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
                    "type": "string"
                },
                "category": {
                    "type": "string"
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
                "name_key": {
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
                }
            }
        }
    }
}
