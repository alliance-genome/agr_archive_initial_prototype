class DoAnnotator:

    # get the gene, disease_dataset in bulk, do_dataset
    @staticmethod
    def attach_annotations(gene, disease_dataset):
        gene_id = gene['primaryId']

        if gene_id in disease_dataset:
            gene['Disease'] = disease_dataset[gene_id]
        return gene
