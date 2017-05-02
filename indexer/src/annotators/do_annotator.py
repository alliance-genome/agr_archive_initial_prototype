class DoAnnotator:

    # get the gene, disease_dataset in bulk, do_dataset
    @staticmethod
    def attach_annotations(gene, annots, do_data):

        gene_id = gene['primaryId']
        gene_symbol = gene['symbol']
        species = gene['species']

        # Attach DO terms to genes based on the annotation of DO ids.
        if gene_id in annots:
            gene['diseases'] = annots[gene_id]

            for entry in annots[gene_id]['do_id']:
                if entry in do_data:
                    # Add the gene symbol and species to the main DO dataset under the particular DO id.
                    do_data = DoAnnotator().update_do_dataset(entry, do_data, gene_symbol, species)
        return gene, go_data

    # Attach gene symbols and species to the DO dataset.
    @staticmethod
    def update_go_dataset(do_id, do_data, gene_symbol, species):
        if species is not "Danio rerio":
            gene_symbol.upper()

        if gene_symbol not in do_data[do_id]['do_genes']:
            do_data[do_id]['do_genes'].append(gene_symbol)
        if species not in do_data[do_id]['do_species']:
            do_data[do_id]['do_species'].append(species)

        return do_data