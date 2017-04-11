from files import *
from test_check import check_for_test_entry
from mods import MOD

import re

class GeneLoader:
    def get_data(self, gene_data, batch_size, test_set):

        gene_dataset = {}
        list_to_yield = []

        dateProduced = gene_data['metaData']['dateProduced']
        dataProvider = gene_data['metaData']['dataProvider']
        release = None

        if 'release' in gene_data['metaData']:
            release = gene_data['metaData']['release']

        for geneRecord in gene_data['data']:
            cross_references = []
            external_ids = []
            genomic_locations = []
            start = None
            end = None
            strand = None
            name = None

            primary_id = geneRecord['primaryId']

            if geneRecord['taxonId'] == "10116" and not primary_id.startswith("RGD"):
                primary_id = dataProvider + ":" + geneRecord['primaryId']

            if test_set == 'true':
                is_it_test_entry = check_for_test_entry(primary_id)
                if is_it_test_entry == 'false':
                    continue

            if 'crossReferences' in geneRecord:
                for crossRef in geneRecord['crossReferences']:
                    ref_text = crossRef['dataProvider'] + " " + crossRef['id']
                    external_ids.append(ref_text)
                    cross_references.append({"dataProvider": crossRef['dataProvider'], "id": crossRef['id']})
            if 'genomeLocations' in geneRecord:
                for genomeLocation in geneRecord['genomeLocations']:
                    chromosome = genomeLocation['chromosome']
                    assembly = genomeLocation['assembly']
                    if 'startPosition' in genomeLocation:
                        start = genomeLocation['startPosition']
                    if 'endPosition' in genomeLocation:
                        end = genomeLocation['endPosition']
                    if 'strand' in geneRecord['genomeLocations']:
                        strand = genomeLocation['strand']
                    genomic_locations.append(
                        {"chromosome": chromosome, "start": start, "end": end, "strand": strand, "assembly": assembly})

            gene_dataset = {
                "symbol": geneRecord['symbol'],
                "name": geneRecord.get('name'),
                "description": geneRecord.get('description'),
                "synonyms": geneRecord.get('synonyms'),
                "soTermId": geneRecord['soTermId'],
                "soTermName": None,
                "secondaryIds": geneRecord.get('secondaryIds'),
                "geneSynopsis": geneRecord.get('geneSynopsis'),
                "geneSynopsisUrl": geneRecord.get('geneSynopsisUrl'),
                "taxonId": geneRecord['taxonId'],
                "species": self.get_species(geneRecord['taxonId']),
                "external_ids": external_ids,
                "gene_biological_process": [],
                "gene_molecular_function": [],
                "gene_cellular_component": [],
                "genomeLocations": genomic_locations,
                "homologs": [],
                "geneLiteratureUrl": geneRecord.get('geneLiteratureUrl'),
                "name_key": geneRecord['symbol'],
                "primaryId": primary_id,
                "crossReferences": cross_references,
                "href": None,
                "category": "gene",
                "dateProduced": dateProduced,
                "dataProvider": dataProvider,
                "release": release,
                "diseases": []
            }

            # Establishes the number of genes to yield (return) at a time.
            list_to_yield.append(gene_dataset)
            if len(list_to_yield) == batch_size:
                yield list_to_yield
                list_to_yield[:] = [] # Empty the list.

        if len(list_to_yield) > 0:
            yield list_to_yield

    def get_species(self, taxon_id):
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
