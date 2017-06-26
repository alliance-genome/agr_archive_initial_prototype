import json
import argparse
import os
import fnmatch
from mods import MOD


parser = argparse.ArgumentParser(description='Test loader for JSON basic gene info file.')

parser.add_argument('-d', '--data', help='JSON data file', required=True)
args = parser.parse_args()

# def load_genes(self):
genes = MOD.genes


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

path = "data/"

for file in os.listdir(path):
    if fnmatch.fnmatch(file, "*.json"):
        with open(os.path.join(path, file)) as data_file:
            data_content = json.load(data_file)

            for geneRecord in data_content['data']:
                synonyms = []
                crossReferences = {}
                description = None
                external_ids = []
                gene_chromosomes = []
                gene_chromosome_starts = []
                gene_chromosome_ends = []
                gene_chromosome_strands = []
                gene_chromosome_assemblies = []
                genomicLocations = []
                chromosome = None
                start = None
                end = None
                strand = None
                assembly = None
                secondaryIds = []
                geneSynopsis = None
                geneSynopsisUrl = None
                geneLiteratureUrl = None

                if 'crossReferences' in geneRecord:
                    for crossRef in geneRecord['crossReferences']:
                        refText = crossRef['dataProvider'] + " " + crossRef['id']
                        external_ids.append(refText)
                        crossReferences = {"dataProvider": crossRef['dataProvider'], "id": crossRef['id']}
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
                        genomicLocations.append({"chromosome": chromosome, "start": start, "end": end, "strand": strand,
                                                 "assembly": assembly})

                genes[geneRecord['primaryId']] = {
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
                    "species": get_species(geneRecord['taxonId']),
                    "external_ids": external_ids,
                    "gene_biological_process": [],
                    "gene_molecular_function": [],
                    "gene_cellular_component": [],
                    "genomeLocations": genomicLocations,
                    "homologs": [],
                    "geneLiteratureUrl": geneRecord.get('geneLiteratureUrl'),
                    "name_key": geneRecord['name'].lower(),
                    "primaryId": geneRecord['primaryId'],
                    "crossReferences": crossReferences,
                    "href": None,
                    "category": "gene"
                }
                # self.soterm_map[geneRecord['soTermId']] = {"geneId": geneRecord['primaryId']}
        data_file.close()

    # for gene in genes:
    #    print gene

    for key, value in genes.iteritems():
       print key, value
