from intermine.webservice import Service
from mod import MOD


class SGD(MOD):
    species = "Saccharomyces cerevisiae"
    service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")
    path_to_basic_gene_information_file = "data/sgd_gene_info.json"

    @staticmethod
    def gene_href(gene_id):
        return "http://www.yeastgenome.org/locus/" + gene_id + "/overview"

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: SGD=S000000226
        return panther_id.split("=")[1]

    def load_go(self):
        query = SGD.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "symbol", "secondaryIdentifier",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "A")

        print("Fetching go data from Yeastmine...")
        for row in query.rows():
            self.add_go_annotation_to_gene(gene_id=row["primaryIdentifier"], go_id=row["goAnnotation.ontologyTerm.identifier"])

    def load_diseases(self):
        query = SGD.service.new_query("Gene")

        query.add_view(
            "primaryIdentifier", "secondaryIdentifier", "symbol",
            "homologues.homologue.primaryIdentifier", "homologues.homologue.symbol",
            "homologues.homologue.name",
            "homologues.homologue.crossReferences.identifier",
            "homologues.homologue.diseases.identifier",
            "homologues.homologue.diseases.name"
        )

        query.add_sort_order("Gene.symbol", "ASC")
        query.add_constraint("homologues.homologue.crossReferences.source.name", "=", "MIM", code = "D")
        query.add_constraint("homologues.homologue.organism.shortName", "=", "H. sapiens", code = "C")
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "B")
        query.add_constraint("homologues.dataSets.dataSource.name", "=", "Panther", code = "A")

        print("Fetching disease data from Yeastmine...")

        for row in query.rows():
            self.add_disease_annotation_to_gene(gene_id=row["primaryIdentifier"], omim_id='OMIM:' + row["homologues.homologue.diseases.identifier"])

