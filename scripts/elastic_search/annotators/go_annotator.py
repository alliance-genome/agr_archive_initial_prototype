class GoAnnotator:

    def attach_annotations(self, genes, annots, go_data):
        go_blacklist = ("GO:0008150", "GO:0003674", "GO:0005575")
        for annot in annots:
            go_id = annot['go_id']
            gene_id = annot['gene_id']

            if go_id not in go_blacklist and gene_id in genes:
                go_type = go_data[go_id]["go_type"]
                term_name = go_data[go_id]["name"]

                if term_name not in genes[gene_id]["gene_" + go_type]:
                    genes[gene_id]["gene_" + go_type].append(term_name)

        return genes