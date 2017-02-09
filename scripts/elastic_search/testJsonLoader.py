import json
import argparse
from mod import MOD

parser = argparse.ArgumentParser(description='Test loader for JSON basic gene info file.')

parser.add_argument('-d', '--data', help='JSON data file', required=True)
args = parser.parse_args()

# def load_genes(self):
genes = MOD.genes


def getSpecies(taxon_id):
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


data_file_name = args.data
with open(data_file_name) as data_file:
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
        genomicLocations = {}
        chromosome = None
        start = None
        end = None
        strand = None
        assembly = None
        secondaryIds = []
        geneSynopsis = None
        geneSynopsisUrl = None

        if 'synonyms' in geneRecord:
            for synonym in geneRecord['synonyms']:
                synonyms.append(synonym)
        if 'description' in geneRecord:
            description = geneRecord['description']
        if 'crossReferences' in geneRecord:
            for crossRef in geneRecord['crossReferences']:
                refText = crossRef['dataProvider'] + " " + crossRef['id']
                external_ids.append(refText)
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
            genomicLocations = {"chromosome": chromosome, "start": start, "end": end, "strand": strand,
                                "assembly": assembly}
        if 'geneLiteratureUrl' in geneRecord:
            geneLiteratureUrl = geneRecord['geneLiteratureUrl']
        if 'secondaryIds' in geneRecord:
            for secondaryId in geneRecord['secondaryIds']:
                secondaryIds.append(secondaryId)
        if 'geneSynopsis' in geneRecord:
            geneSynopsis = geneRecord['geneSynopsis']
        if 'geneSynopsisUrl' in geneRecord:
            geneSynopsisUrl = geneRecord['geneSynopsisUrl']

        # TODO: maybe this method can be generic - running thru the dictionary and adding key:value pairs based on the JSON object now that the mapping.py matches the JSON schema.
        genes[geneRecord['primaryId']] = {
            "symbol": geneRecord['symbol'],
            "name": geneRecord['name'],
            "description": description,
            "synonyms": synonyms,
            "soTermId": geneRecord['soTermId'],
            "soTermName": None,
            "secondaryIds": secondaryIds,
            "geneSynopsis": geneSynopsis,
            "geneSynopsisUrl": geneSynopsisUrl,
            "gene_chromosomes": gene_chromosomes,
            "gene_chromosome_starts": gene_chromosome_starts,
            "gene_chromosome_ends": gene_chromosome_ends,
            "gene_chromosome_strand": gene_chromosome_strands,
            "taxonId": geneRecord['taxonId'],
            "species": getSpecies(geneRecord['taxonId']),
            "external_ids": external_ids,
            "gene_biological_process": [],
            "gene_molecular_function": [],
            "gene_cellular_component": [],
            "genomeLocations": genomicLocations,
            "homologs": [],
            "geneLiteratureUrl": geneLiteratureUrl,
            "name_key": geneRecord['name'].lower(),
            "primaryId": geneRecord['primaryId'],
            "href": None,
            "category": "gene"
        }

    # for gene in genes:
    #    print gene

    # for key, value in genes.iteritems():
    #   print key, value
