from mod import MOD


class Human(MOD):
    species = "Homo sapiens"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=" + gene_id

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: HGNC=974
        return panther_id.replace("=", ":")
