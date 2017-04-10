class GoAnnotator:

    @staticmethod
    def attach_annotations(gene, annots, go_data):
        go_blacklist = ("GO:0008150", "GO:0003674", "GO:0005575")
        gene_id = gene['primaryId']
        gene_symbol = gene['symbol']
        species = gene['species']

        # Attach GO terms to genes based on the annotation of GO ids.
        if gene_id in annots:
            for entry in annots[gene_id]['go_id']:
                if entry not in go_blacklist and entry in go_data:
                    term_name = go_data[entry]['name']
                    go_type = go_data[entry]['go_type']
                    # Add the gene symbol and species to the main GO dataset under the particular GO id.
                    go_data = GoAnnotator().update_go_dataset(entry, go_data, gene_symbol, species)  
                    if term_name not in gene['gene_' + go_type]:
                        gene['gene_' + go_type].append(term_name)
        return (gene, go_data)

    # Attach gene symbols and species to the GO dataset.
    @staticmethod
    def update_go_dataset(go_id, go_data, gene_symbol, species):
        if species is not "Danio rerio":
            gene_symbol.upper()  

        if gene_symbol not in go_data[go_id]['go_genes']:
            go_data[go_id]['go_genes'].append(gene_symbol)
        if species not in go_data[go_id]['go_species']:
            go_data[go_id]['go_species'].append(species)

        return go_data