from loaders.gene_loader import GeneLoader
from intermine.webservice import Service
from files import *
from mod import MOD


class SGD(MOD):
    species = "Saccharomyces cerevisiae"

    def __init__(self):
        self.service = Service("http://yeastmine.yeastgenome.org/yeastmine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.yeastgenome.org/locus/" + gene_id + "/overview"

    @staticmethod
    def get_organism_names():
        return ["Saccharomyces cerevisiae", "S. cerevisiae", "YEAST"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: SGD=S000000226
        return panther_id.split("=")[1]

    def load_genes(self):
        path = "tmp"
        S3File("mod-datadumps", "SGD_0.3.0_1.tar.gz", path).download()
        TARFile(path, "SGD_0.3.0_1.tar.gz").extract_all()
        return GeneLoader(path + "/SGD_0.3_basicGeneInformation.json").get_data()

    def load_go(self):
        query = self.service.new_query("Gene")
        query.add_view(
            "primaryIdentifier", "symbol", "secondaryIdentifier",
            "goAnnotation.ontologyTerm.identifier", "goAnnotation.ontologyTerm.name",
            "goAnnotation.ontologyTerm.namespace"
        )
        query.add_constraint("organism.shortName", "=", "S. cerevisiae", code = "A")

        print("Fetching go data from Yeastmine...")
        list = []
        for row in query.rows():
            list.append({"gene_id": row["primaryIdentifier"], "go_id": row["goAnnotation.ontologyTerm.identifier"], "species": SGD.species})
        return list

    def load_diseases(self):
        query = self.service.new_query("Gene")

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
        list = []
        for row in query.rows():
            list.append({"gene_id": row["primaryIdentifier"], "omim_id":'OMIM:' + row["homologues.homologue.diseases.identifier"], "species": SGD.species})
        return list
