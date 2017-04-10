mapping_schema = {
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
                    "autocomplete_search": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": "lowercase"
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
                "primaryId": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "fields": {
                        "symbol": {
                            "type": "text",
                            "analyzer": "symbols"
                        },
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search"
                        },
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "taxonId": {
                    "type": "keyword"
                },
                "symbol": {
                    "type": "text",
                    "analyzer": "symbols",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search"
                        },
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "systematicName": {
                    "type": "text",
                    "analyzer": "symbols"
                },
                "geneSynopsis": {
                    "type": "text"
                },
                "geneSynopsisUrl": {
                    "type": "keyword"
                },
                "geneLiteratureUrl": {
                    "type": "keyword"
                },
                "soTermId": {
                    "type": "keyword"
                },
                "synonyms": {
                    "type": "text",
                    "analyzer": "symbols",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete",
                            "search_analyzer": "autocomplete_search"
                        },
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "crossReferences": {
                    "properties": {
                        "dataProvider": {
                            "type": "keyword"
                        },
                        "id": {
                            "type": "keyword"
                        }
                    }
                },
                "genomeLocations": {
                    "properties": {
                        "assembly": {
                            "type": "keyword"
                        },
                        "startPosition": {
                            "type": "integer"
                        },
                        "endPosition": {
                            "type": "integer"
                        },
                        "chromosome": {
                            "type": "keyword"
                        },
                        "strand": {
                            "type": "keyword"
                        }
                    }
                },
                "secondaryIds": {
                    "type": "keyword"
                },

                "metaData": {
                    "properties": {
                        "dateProduced": {
                            "type": "date"
                         },
                        "dataProvider": {
                            "type": "keyword"
                        },
                        "release": {
                            "type": "keyword"
                        }
                    }
                },
                "description": {
                    "type": "text"
                },
                "external_ids": {
                    "type": "text",
                    "analyzer": "symbols"
                },
                "gene_biological_process": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        },
                        "symbol": {
                            "type": "text",
                            "analyzer": "symbols"
                        }

                    }
                },
                "gene_molecular_function": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        },
                        "symbol": {
                            "type": "text",
                            "analyzer": "symbols"
                        }

                    }
                },
                "gene_cellular_component": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        },
                        "symbol": {
                            "type": "text",
                            "analyzer": "symbols"
                        }

                    }
                },
                "species": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "href": {
                    "type": "text",
                    "analyzer": "symbols"
                },
                "category": {
                    "type": "keyword",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        },
                        "symbol": {
                            "type": "text",
                            "analyzer": "symbols"
                        }
                    }
                },
                "go_type": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "go_genes": {
                    "type": "text",
                    "analyzer": "symbols",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "go_species": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "disease_genes": {
                    "type": "text",
                    "analyzer": "symbols",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "disease_species": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "disease_synonyms": {
                    "type": "text"
                },
                "id": {
                    "type": "text",
                    "analyzer": "symbols"
                },
                "name_key": {
                    "type": "text",
                    "analyzer": "symbols",
                    "fields": {
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete"
                        }
                    }
                },
                "diseases": {
                    "properties": {
                        "do_id": {
                            "type": "text",
                            "analyzer": "symbols"
                        },
                        "do_name": {
                            "type": "text"
                        },
                        "associationType": {
                            "type": "text"
                        },
                        "evidence": {
                            "properties": {
                                "evidenceCode": {
                                    "type": "text"
                                },
                                "pubs": {
                                    "properties": {
                                        "pubmedId": {
                                            "type": "text"
                                        },
                                        "publicationModId": {
                                            "type": "text"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
