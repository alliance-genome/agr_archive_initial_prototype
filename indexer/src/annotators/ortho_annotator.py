class OrthoAnnotator:

    @staticmethod
    def attach_annotations(gene, ortho_dataset):
        gene_id = gene['primaryId']

        if gene_id in ortho_dataset:
            gene['Orthology'] = ortho_dataset[gene_id]
        return gene