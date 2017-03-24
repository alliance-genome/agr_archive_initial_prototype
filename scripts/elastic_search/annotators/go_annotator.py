class GoAnnotator:

    @staticmethod
    def attach_annotations(gene, annots, go_data):
        go_blacklist = ("GO:0008150", "GO:0003674", "GO:0005575")
        gene_id = gene['primaryId']

        if gene_id in annots:
            for entry in annots[gene_id]['go_id']:
                if entry not in go_blacklist and entry in go_data:
                    term_name = go_data[entry]['name']
                    go_type = go_data[entry]['go_type']
                    if term_name not in gene['gene_' + go_type]:
                        gene['gene_' + go_type].append(term_name)