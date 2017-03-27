from files import *
from mods import MOD

import re

class GeneLoader:
    def get_data(self, gene_data):
        
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
                    genomic_locations.append(
                        {"chromosome": chromosome, "start": start, "end": end, "strand": strand, "assembly": assembly})

            primary_id = geneRecord['primaryId']

            if geneRecord['taxonId'] == "10116" and not primary_id.startswith("RGD"):
                primary_id = dataProvider + ":" + geneRecord['primaryId']

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
                "name_key": geneRecord['symbol'],
                "primaryId": primary_id,
                "crossReferences": cross_references,
                "href": None,
                "category": "gene",
                "dateProduced": dateProduced,
                "dataProvider": dataProvider,
                "release": release
            }

            # Establishes the number of genes to yield (return) at a time.
            list_to_yield.append(gene_dataset)
            if len(list_to_yield) == 5000:
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
