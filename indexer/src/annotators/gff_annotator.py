import pprint

class GFFAnnotator:

    @staticmethod
    def attach_annotations(gene, gff_dataset):
        gene_id = gene['primaryId']

        if gene_id in gff_dataset:
            gene['gff'] = gff_dataset[gene_id]
        return gene