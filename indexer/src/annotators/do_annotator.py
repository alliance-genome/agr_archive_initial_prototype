class DoAnnotator:

    # get the gene, disease_dataset in bulk, do_dataset
    @staticmethod
    def attach_annotations(gene, disease_dataset, do_dataset):

        gene_id = gene['primaryId']
        #gene_symbol = gene['symbol']
        #species = gene['species']

        if gene_id in disease_dataset:
            gene['diseases'] = disease_dataset[gene_id]

        if gene_id in disease_dataset:
            for d_annot in disease_dataset[gene_id]:
                d_annot['do_name'] = do_dataset[d_annot['do_id']]['name']

        return gene

