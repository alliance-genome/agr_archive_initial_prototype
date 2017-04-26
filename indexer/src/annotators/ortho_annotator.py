class OrthoAnnotator:
    @staticmethod
    def attach_annotations(gene, ortho_dataset):
        if gene['taxonId'] == "NCBITaxon:10090" or "NCBITaxon:9606":
            gene_id = gene['primaryId']
        else:
            global_id = gene['primaryId']
            gene_id = global_id.split(":")[1]
        if gene_id in ortho_dataset:
            gene['Orthology'] = ortho_dataset[gene_id]
        return gene
