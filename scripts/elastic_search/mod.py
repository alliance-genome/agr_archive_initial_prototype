import csv
import pickle
import requests
import os
import re
import json
import fnmatch
from elasticsearch import Elasticsearch


class MOD():

    INDEX_NAME = os.environ['ES_INDEX']

    DOC_TYPE = 'searchable_item'

    go_blacklist = ("GO:0008150", "GO:0003674", "GO:0005575")
    path_to_basic_gene_information_file = None
    gene_bkp_filename = "data/genes_bkp.pickle"
    go_bkp_filename = "data/go_bkp.pickle"
    so_bkp_filename = "data/so_bkp.pickle"
    diseases_bkp_filename = "data/diseases_bkp.pickle"

    go_dataset = {}
    so_dataset = {}
    omim_dataset = {}

    genes = {}
    go = {}
    diseases = {}
    soterm_map = {}

    def __init__(self):
        self._load_omim_dataset()
        self._load_go_dataset()
        self._load_so_dataset()
        self.es = Elasticsearch(os.environ['ES_URI'], retry_on_timeout=True)

    @staticmethod
    def get_species(taxon_id):
        if taxon_id in ("7955"):
            return "Danio rerio"
        elif taxon_id in ("6239"):
            return "Caenorhabditis elegans"
        elif taxon_id in ("10090"):
            return "Mus musculus"
        elif taxon_id in ("10116"):
            return "Rattus norvegicus"
        elif taxon_id in ("559292"):
            return "Saccharomyces cerevisiae"
        elif taxon_id in ("7227"):
            return "Drosophila melanogaster"
        elif taxon_id in ("9606"):
            return "Homo sapiens"
        else:
            return None

    def load_genes(self):
        path = "data/"
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, "*.json"):
                with open(os.path.join(path, file)) as data_file:
                    data_content = json.load(data_file)

                    dateProduced = data_content['metaData']['dateProduced']
                    dataProvider = data_content['metaData']['dataProvider']
                    release = None

                    if 'release' in data_content['metaData']:
                        release = data_content['metaData']['release']

                    for geneRecord in data_content['data']:
                        cross_references = []
                        external_ids = []
                        gene_chromosomes = []
                        gene_chromosome_starts = []
                        gene_chromosome_ends = []
                        gene_chromosome_strands = []
                        gene_chromosome_assemblies = []
                        genomic_locations = []
                        start = None
                        end = None
                        strand = None
                        name = None

                        if 'crossReferences' in geneRecord:
                            for crossRef in geneRecord['crossReferences']:
                                ref_text = crossRef['dataProvider'] + " " + crossRef['id']
                                external_ids.append(ref_text)
                                cross_references.append({"dataProvider": crossRef['dataProvider'], "id": crossRef['id']})
                        if 'genomeLocations' in geneRecord:
                            for genomeLocation in geneRecord['genomeLocations']:
                                gene_chromosomes.append(genomeLocation['chromosome'])
                                chromosome = genomeLocation['chromosome']
                                gene_chromosome_assemblies.append(genomeLocation['assembly'])
                                assembly = genomeLocation['assembly']
                                if 'start' in genomeLocation:
                                    gene_chromosome_starts.append(genomeLocation['start'])
                                    start = genomeLocation['start']
                                if 'end' in geneRecord['genomeLocations']:
                                    gene_chromosome_ends.append(genomeLocation['end'])
                                    end = genomeLocation['end']
                                if 'strand' in geneRecord['genomeLocations']:
                                    gene_chromosome_strands.append(genomeLocation['strand'])
                                    strand = genomeLocation['strand']
                                genomic_locations.append({"chromosome": chromosome, "start": start, "end": end,
                                                         "strand": strand, "assembly": assembly})

                        self.genes[geneRecord['primaryId']] = {
                            "symbol": geneRecord['symbol'],
                            "name": geneRecord.get('name'),
                            "description": geneRecord.get('description'),
                            "synonyms": geneRecord.get('synonyms'),
                            "soTermId": geneRecord['soTermId'],
                            "soTermName": None,
                            "secondaryIds": geneRecord.get('secondaryIds'),
                            "geneSynopsis": geneRecord.get('geneSynopsis'),
                            "geneSynopsisUrl": geneRecord.get('geneSynopsisUrl'),
                            "gene_chromosomes": gene_chromosomes,
                            "gene_chromosome_starts": gene_chromosome_starts,
                            "gene_chromosome_ends": gene_chromosome_ends,
                            "gene_chromosome_strand": gene_chromosome_strands,
                            "taxonId": geneRecord['taxonId'],
                            "species": self.get_species(geneRecord['taxonId']),
                            "external_ids": external_ids,
                            "gene_biological_process": [],
                            "gene_molecular_function": [],
                            "gene_cellular_component": [],
                            "genomeLocations": genomic_locations,
                            "homologs": [],
                            "geneLiteratureUrl": geneRecord.get('geneLiteratureUrl'),
                            "name_key": name,
                            "primaryId": geneRecord['primaryId'],
                            "crossReferences": cross_references,
                            "href": None,
                            "category": "gene",
                            "dateProduced": dateProduced,
                            "dataProvider": dataProvider,
                            "release": release
                        }
                        #self.soterm_map[geneRecord['soTermId']] = {"geneId": geneRecord['primaryId']}
                data_file.close()


    @staticmethod
    def factory(organism):
        from sgd import SGD
        from zfin import ZFIN
        from worm import WormBase
        from fly import FlyBase
        from mouse import MGI
        from rat import RGD
        from human import Human

        if organism in ("Saccharomyces cerevisiae", "S. cerevisiae", "YEAST"):
            return SGD()
        elif organism in ("Danio rerio", "D. rerio", "DANRE"):
            return ZFIN()
        elif organism in ("Caenorhabditis elegans", "C. elegans", "CAEEL"):
            return WormBase()
        elif organism in ("Drosophila melanogaster", "D. melanogaster", "DROME"):
            return FlyBase()
        elif organism in ("Mus musculus", "M. musculus", "MOUSE"):
            return MGI()
        elif organism in ("Rattus norvegicus", "R. norvegicus", "RAT"):
            return RGD()
        elif organism in ("Homo sapiens", "H. sapiens", "HUMAN"):
            return Human()
        else:
            return None

    @staticmethod
    def _process_gene_id_from_panther(gene_ids_panther, genes):
        gene_ids = gene_ids_panther.split("|")
        mod = MOD.factory(gene_ids[0])

        if mod is None:
            return None

        gene_id = MOD.factory(gene_ids[0]).gene_id_from_panther(gene_ids[1])

        gene_symbol = ""
        if mod.__class__.__module__ == "human":
            gene_symbol = gene_id
        else:
            if gene_id not in genes:
                return None
            else:
                gene_symbol = genes[gene_id]["symbol"]

        return {
            "id": gene_id,
            "symbol": gene_symbol,
            "href": mod.gene_href(gene_id),
            "species": mod.species
        }

    def load_homologs(self):
        from human import Human

        print "Loading orthologs from Panther file (data/RefGenomeOrthologs) ..."
        with open("data/RefGenomeOrthologs", "r") as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                gene_1 = MOD._process_gene_id_from_panther(row[0], self.genes)
                gene_2 = MOD._process_gene_id_from_panther(row[1], self.genes)

                if gene_1 is None or gene_2 is None:
                    continue

                if gene_1["species"] != Human.species:
                    if "homologs" not in self.genes[gene_1["id"]]:
                        self.genes[gene_1["id"]]["homologs"] = []

                    self.genes[gene_1["id"]]["homologs"].append({
                        "symbol": gene_2["symbol"],
                        "href": gene_2["href"],
                        "species": gene_2["species"],
                        "relationship_type": row[2],
                        "ancestral": row[3],
                        "panther_family": row[4]
                    })

                if gene_2["species"] != Human.species:
                    if "homologs" not in self.genes[gene_2["id"]]:
                        self.genes[gene_2["id"]]["homologs"] = []

                    self.genes[gene_2["id"]]["homologs"].append({
                        "symbol": gene_1["symbol"],
                        "href": gene_1["href"],
                        "species": gene_1["species"],
                        "relationship_type": row[2],
                        "ancestral": row[3],
                        "panther_family": row[4]
                    })

    def _load_omim_dataset(self):
        if MOD.omim_dataset != {}:
            return

        print "loading OMIM dataset from file (data/OMIM_diseases.txt) ..."
        with open("data/OMIM_diseases.txt", "r") as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)
            next(reader, None)
            next(reader, None)

            for row in reader:
                if len(row) < 3:
                    continue

                name_column = row[2].split(";")
                name = name_column[0].strip()
                if len(name_column) > 1:
                    symbol = name_column[1].strip()
                else:
                    symbol = None

                synonyms = []

                for r in (row[3], row[4]):
                    if r == '':
                        continue

                    alternative_names = r.split(";;")

                    for alt_name_symbol in alternative_names:
                        alt_name_symbol = alt_name_symbol.split(";")
                        alt_name = alt_name_symbol[0].strip().lower()
                        if len(alt_name_symbol) > 1:
                            alt_symbol = ", " + alt_name_symbol[1].strip()
                        else:
                            alt_symbol = ""

                        synonyms.append(alt_name + alt_symbol)

                MOD.omim_dataset["OMIM:" + row[1]] = {
                    "prefix": row[0],
                    "name": name.lower(),
                    "symbol": symbol,
                    "disease_synonyms": synonyms
                }

    def _load_go_dataset(self):
        if MOD.go_dataset != {}:
            return

        print "Loading GO dataset from file (data/go.obo) ..."
        with open("data/go.obo", "r") as f:
            creating_term = None

            for line in f:
                line = line.strip()

                if line == "[Term]":
                    creating_term = True
                elif creating_term:
                    key = (line.split(":")[0]).strip()
                    value = ("".join(":".join(line.split(":")[1:]))).strip()

                    if key == "id":
                        creating_term = value
                        MOD.go_dataset[creating_term] = {}
                    else:
                        if key == "synonym":
                            if value.split(" ")[-2] == "EXACT":
                                value = (" ".join(value.split(" ")[:-2]))[1:-1]
                            else:
                                continue
                        if key == "def":
                            m = re.search('\"(.+)\"', value)
                            value = m.group(1)

                        if key in MOD.go_dataset[creating_term]:
                            MOD.go_dataset[creating_term][key].append(value)
                        else:
                            MOD.go_dataset[creating_term][key] = [value]

    def _load_so_dataset(self):
        if MOD.so_dataset != {}:
            return

        print "Loading SO dataset from file (data/so.obo) ..."
        with open("data/so.obo", "r") as f:
            creating_term = None

            for line in f:
                line = line.strip()

                if line == "[Term]":
                    creating_term = True
                elif creating_term:
                    key = (line.split(":")[0]).strip()
                    value = ("".join(":".join(line.split(":")[1:]))).strip()

                    if key == "id":
                        creating_term = value
                        MOD.so_dataset[creating_term] = {}
                    else:
                        if key == "synonym":
                            if value.split(" ")[-2] == "EXACT":
                                value = (" ".join(value.split(" ")[:-2]))[1:-1]
                            else:
                                continue
                        if key == "def":
                            m = re.search('\"(.+)\"', value)
                            value = m.group(1)

                        if key in MOD.so_dataset[creating_term]:
                            MOD.so_dataset[creating_term][key].append(value)
                        else:
                            MOD.so_dataset[creating_term][key] = [value]

    def add_go_annotation_to_gene(self, gene_id, go_id):
        if go_id not in self.go_dataset or go_id in MOD.go_blacklist or gene_id not in self.genes:
            return

        gene_symbol = self.genes[gene_id]["symbol"].upper()

        if go_id in self.go:
            if gene_symbol not in self.go[go_id]["go_genes"]:
                self.go[go_id]["go_genes"].append(gene_symbol)
            if self.species not in self.go[go_id]["go_species"]:
                self.go[go_id]["go_species"].append(self.species)
        else:
            self.go[go_id] = {
                "go_genes": [gene_symbol],
                "go_species": [self.species],

                "name": self.go_dataset[go_id]["name"][0],
                "description": self.go_dataset[go_id]["def"][0],
                "go_type": self.go_dataset[go_id]["namespace"][0],
                "go_synonyms": self.go_dataset[go_id].get("synonym"),

                "name_key": self.go_dataset[go_id]["name"][0],
                "id": go_id,
                "href": "http://amigo.geneontology.org/amigo/term/" + go_id,
                "category": "go"
            }
        # appends go terms to the go namespace collections on gene dictionary created in load_genes() for each mod

        go_type = self.go[go_id]["go_type"]
        term_name = self.go[go_id]["name"]

        if term_name not in self.genes[gene_id]["gene_" + go_type]:
            self.genes[gene_id]["gene_" + go_type].append(term_name)

    def add_disease_annotation_to_gene(self, gene_id, omim_id):
        if omim_id not in self.omim_dataset or gene_id not in self.genes:
            return

        gene_symbol = self.genes[gene_id]["symbol"].upper()

        if omim_id in self.diseases:
            if gene_symbol not in self.diseases[omim_id]["disease_genes"]:
                self.diseases[omim_id]["disease_genes"].append(gene_symbol)
            if self.species not in self.diseases[omim_id]["disease_species"]:
                self.diseases[omim_id]["disease_species"].append(self.species)
        else:
            self.diseases[omim_id] = {
                "disease_genes": [gene_symbol],
                "disease_species": [self.species],

                "name": self.omim_dataset[omim_id]["name"],
                "symbol": self.omim_dataset[omim_id]["symbol"],
                "disease_synonyms": self.omim_dataset[omim_id]["disease_synonyms"],

                "name_key": self.omim_dataset[omim_id]["name"],
                "id": omim_id,
                "key": omim_id,
                "href": "http://omim.org/entry/" + omim_id.split(":")[1],
                "category": "disease"
            }

    def load_from_file(self, filename):
        if os.path.isfile(filename):
            with open(filename, "rb") as f:
                return pickle.load(f)
        return None

    def load_data_from_file(self):
        print "Loading genes from file (" + self.gene_bkp_filename + ") ..."
        self.genes = self.load_from_file(self.gene_bkp_filename)

        print "Loading go from file (" + self.go_bkp_filename + ") ..."
        self.go = self.load_from_file(self.go_bkp_filename)

        print "Loading diseases from file (" + self.diseases_bkp_filename + ") ..."
        self.diseases = self.load_from_file(self.diseases_bkp_filename)

        if self.genes is None or self.go is None or self.diseases is None:
            print ("Fail loading data from backup")

    def save_dict_into_file(self, data, filename):
        with open(filename, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def save_into_file(self):
        print "Saving genes into file (" + self.gene_bkp_filename + ") ..."
        self.save_dict_into_file(self.genes, self.gene_bkp_filename)

        print "Saving go into file (" + self.go_bkp_filename + ") ..."
        self.save_dict_into_file(self.go, self.go_bkp_filename)

        print "Saving diseases into file (" + self.diseases_bkp_filename + ") ..."
        self.save_dict_into_file(self.diseases, self.diseases_bkp_filename)

    def delete_mapping(self):
        print "Deleting mapping..."
        response = requests.delete(os.environ['ES_URI'] + self.INDEX_NAME + "/")
        if response.status_code != 200:
            print "ERROR: " + str(response.json())
        else:
            print "SUCCESS"

    def put_mapping(self):
        from mapping import mapping

        print "Putting mapping... "
        response = requests.put(os.environ['ES_URI'] + self.INDEX_NAME + "/", json=mapping)
        if response.status_code != 200:
            print "ERROR: " + str(response.json())
        else:
            print "SUCCESS"

    def index_into_es(self, data):
        bulk_data = []

        for id in data:
            bulk_data.append({
                'index': {
                    '_index': self.INDEX_NAME,
                    '_type': self.DOC_TYPE,
                    '_id': id
                }
            })
            bulk_data.append(data[id])

            if len(bulk_data) == 300:
                self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)
                bulk_data = []

        if len(bulk_data) > 0:
            self.es.bulk(index=self.INDEX_NAME, body=bulk_data, refresh=True)

    def index_genes_into_es(self):
        print "Indexing genes into ES..."
        self.index_into_es(self.genes)

    def index_go_into_es(self):
        print "Indexing go into ES..."
        self.index_into_es(self.go)

    def index_diseases_into_es(self):
        print "Indexing diseases into ES..."
        self.index_into_es(self.diseases)

    def index_all_into_es(self):
        self.index_genes_into_es()
        self.index_go_into_es()
        self.index_diseases_into_es()
