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
            crossReferences = []
            external_ids = []
            genomic_locations = []
            start = None
            end = None
            strand = None
            name = None
            modCrossReference = []

            primary_id = geneRecord['primaryId']
            global_id = geneRecord['primaryId']

            #this can be removed when all MODs have their prefixed id files
            if ':' in geneRecord['primaryId']:
                local_id = global_id.split(":")[1]
            else:
                local_id = global_id

            modCrossReference = {"id": global_id, "globalCrossRefId": global_id, "localId": local_id, "crossrefCompleteUrl": self.get_complete_url(local_id, global_id)}
            if geneRecord['taxonId'] == "NCBITaxon:9606" or geneRecord['taxonId'] == "NCBITaxon:10090":
                local_id = geneRecord['primaryId']

            if test_set == True:
                is_it_test_entry = check_for_test_entry(primary_id)
                if is_it_test_entry == False:
                    continue

            if 'crossReferenceIds' in geneRecord:
                for crossRef in geneRecord['crossReferenceIds']:
                    external_ids.append(crossRef)
                    #this can be simplified when GO YAML reused for AGR has helper fields.
                    if ':' in crossRef:
                        local_crossref_id = crossRef.split(":")[1]
                        crossReferences.append({"id": crossRef, "globalCrossrefId": crossRef, "localId": local_crossref_id, "crossrefCompleteUrl": self.get_complete_url(local_crossref_id, crossRef)})
                    else:
                        local_crossref_id = crossRef
                        crossReferences.append(
                            {"id": crossRef, "globalCrossrefId": crossRef, "localId": local_crossref_id,
                             "crossrefCompleteUrl": self.get_complete_url(local_crossref_id, crossRef)})
            if 'genomeLocations' in geneRecord:
                for genomeLocation in geneRecord['genomeLocations']:
                    chromosome = genomeLocation['chromosome']
                    assembly = genomeLocation['assembly']
                    if 'startPosition' in genomeLocation:
                        start = genomeLocation['startPosition']
                    else:
                        start = None
                    if 'endPosition' in genomeLocation:
                        end = genomeLocation['endPosition']
                    else:
                        end = None
                    if 'strand' in geneRecord['genomeLocations']:
                        strand = genomeLocation['strand']
                    else:
                        strand = None
                    genomic_locations.append(
                        {"chromosome": chromosome, "start": start, "end": end, "strand": strand, "assembly": assembly})

            gene_dataset = {
                "symbol": geneRecord['symbol'],
                "name": geneRecord.get('name'),
                "description": geneRecord.get('description'),
                "synonyms": geneRecord.get('synonyms'),
                "soTermId": geneRecord['soTermId'],
                "soTermName": None,
                "diseases": [],
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
                "geneLiteratureUrl": geneRecord.get('geneLiteratureUrl'),
                "name_key": geneRecord['symbol'],
                "primaryId": primary_id,
                "crossReferences": crossReferences,
                "modCrossReference": modCrossReference,
                "category": "gene",
                "dateProduced": dateProduced,
                "dataProvider": dataProvider,
                "release": release,
                "href": None
            }

            # Establishes the number of genes to yield (return) at a time.
            list_to_yield.append(gene_dataset)
            if len(list_to_yield) == batch_size:
                yield list_to_yield
                list_to_yield[:] = []  # Empty the list.

        if len(list_to_yield) > 0:
            yield list_to_yield

    def get_species(self, taxon_id):
        if taxon_id in ("NCBITaxon:7955"):
            return "Danio rerio"
        elif taxon_id in ("NCBITaxon:6239"):
            return "Caenorhabditis elegans"
        elif taxon_id in ("NCBITaxon:10090"):
            return "Mus musculus"
        elif taxon_id in ("NCBITaxon:10116"):
            return "Rattus norvegicus"
        elif taxon_id in ("NCBITaxon:559292"):
            return "Saccharomyces cerevisiae"
        elif taxon_id in ("NCBITaxon:7227"):
            return "Drosophila melanogaster"
        elif taxon_id in ("NCBITaxon:9606"):
            return "Homo sapiens"
        else:
            return None

    def get_complete_url (self, local_id, global_id):

        complete_url = None

        if 'MGI' in global_id:
            complete_url = 'http://www.informatics.jax.org/accession/' + local_id
        if 'RGD' in global_id:
            complete_url = 'http://rgd.mcw.edu/rgdweb/search/search.html?term=' + local_id
        if 'SGD' in global_id:
            complete_url = 'http://www.yeastgenome.org/locus/' + local_id
        if 'FB' in global_id:
            complete_url = 'http://flybase.org/reports/' + local_id + '.html'
        if 'ZFIN' in global_id:
            complete_url = 'http://zfin.org/' + local_id
        if 'WB:' in global_id:
            complete_url = 'http://www.wormbase.org/species/c_elegans/gene/' + local_id
        if 'HGNC:' in global_id:
            complete_url = 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=' + local_id
        if 'NCBI_Gene' in global_id:
            complete_url = 'https://www.ncbi.nlm.nih.gov/gene/' + local_id
        if 'UniProtKB' in global_id:
            complete_url = 'http://www.uniprot.org/uniprot/' + local_id
        if 'ENSEMBL' in global_id:
            complete_url = 'http://www.ensembl.org/id/' + local_id
        if 'RNAcentral' in global_id:
            complete_url = 'http://rnacentral.org/rna/' + local_id
        if 'PMID' in global_id:
            complete_url = 'https://www.ncbi.nlm.nih.gov/pubmed/' + local_id
        if 'SO:' in global_id:
            complete_url = 'http://www.sequenceontology.org/browser/current_svn/term/' + local_id
        if 'DRSC' in global_id:
            complete_url = None

        return complete_url