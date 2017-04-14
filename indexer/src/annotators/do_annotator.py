class DoAnnotator:

    # get the gene, disease_dataset in bulk, do_dataset
    @staticmethod
    def attach_annotations(gene, disease_dataset):

        gene_id = gene['primaryId']
        gene_symbol = gene['symbol']
        species = gene['species']

        if gene_id in disease_dataset:
            gene['diseases'] = disease_dataset[gene_id]

        # if gene_id in disease_dataset:
        #     for d_annot in disease_dataset[gene_id]['do_id']:
        #         do_dataset = DoAnnotator().update_do_dataset(d_annot, do_dataset, gene_symbol, species)
        # return gene, do_dataset
            return gene

    # Attach gene symbols and species to the GO dataset.
    # @staticmethod
    # def update_do_dataset(do_id, do_dataset, gene_symbol, species):
    #     if species is not "Danio rerio":
    #         gene_symbol.upper()
    #
    #     if gene_symbol not in do_dataset[do_id]['do_genes']:
    #         do_dataset[do_id]['do_genes'].append(gene_symbol)
    #     if species not in do_dataset[do_id]['do_species']:
    #         do_dataset[do_id]['do_species'].append(species)
    #
    #     return do_dataset
