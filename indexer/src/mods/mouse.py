from mod import MOD
from files import *
from loaders.gene_loader import GeneLoader
from intermine.webservice import Service

import json

class MGI(MOD):
    species = "Mus musculus"

    def __init__(self):
        self.service = Service("http://www.mousemine.org/mousemine/service")

    @staticmethod
    def gene_href(gene_id):
        return "http://www.informatics.jax.org/marker/" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Mus musculus", "M. musculus", "MOUSE"]

    @staticmethod
    def gene_id_from_panther(panther_id):
        # example: MGI=MGI=1924210
        return ":".join(panther_id.split("=")[1:]).strip()

    def load_genes(self):
        path = "tmp"
        S3File("mod-datadumps", "MGI_0.3.0_1.tar.gz", path).download()
        TARFile(path, "MGI_0.3.0_1.tar.gz").extract_all()
        return GeneLoader(path + "/MGI_0.3_basicGeneInformation.json").get_data()

    def load_go(self):
        query = self.service.new_query("GOTerm")
        query.add_constraint("ontologyAnnotations.subject", "SequenceFeature")
        query.add_view(
            "identifier", "name", "namespace", "ontologyAnnotations.qualifier",
            "ontologyAnnotations.subject.primaryIdentifier",
            "ontologyAnnotations.subject.symbol", "synonyms.name", "synonyms.type"
        )
        query.outerjoin("ontologyAnnotations")
        query.outerjoin("ontologyAnnotations.subject")
        query.outerjoin("synonyms")

        print ("Fetching go data from MouseMine...")

        list = []
        for row in query.rows():
            list.append({"gene_id": row["ontologyAnnotations.subject.primaryIdentifier"], "go_id": row["identifier"], "species": MGI.species})
        return list

    def load_diseases(self):
        query = self.service.new_query("OMIMTerm")
        query.add_constraint("ontologyAnnotations.subject", "SequenceFeature")
        query.add_view(
            "identifier", "name", "synonyms.name", "synonyms.type",
            "ontologyAnnotations.qualifier",
            "ontologyAnnotations.subject.primaryIdentifier",
            "ontologyAnnotations.subject.symbol"
        )
        query.add_constraint("ontologyAnnotations.subject.organism.taxonId", "=", "10090", code = "A")
        query.outerjoin("synonyms")
        query.outerjoin("ontologyAnnotations")

        print ("Fetching disease data from MouseMine...")
        
        list = []
        for row in query.rows():
            list.append({"gene_id": row["ontologyAnnotations.subject.primaryIdentifier"], "omim_id": row["identifier"], "species": MGI.species})
        return list
