
class DiseaseGeneAnnotLoader:
    
    def __init__(self, genes, omim_data):
        self.diseases = {}
        self.genes = genes
        self.omim_dataset = omim_data

    def attach_annotations(self, annots):
        for annot in annots:
            self.add_disease_annotation_to_gene(annot["gene_id"], annot["omim_id"], annot["species"])
        return self.diseases

    def add_disease_annotation_to_gene(self, gene_id, omim_id, species):
        if omim_id not in self.omim_dataset or gene_id not in self.genes:
            return

        gene_symbol = self.genes[gene_id]["symbol"].upper()

        if omim_id in self.diseases:
            if gene_symbol not in self.diseases[omim_id]["disease_genes"]:
                self.diseases[omim_id]["disease_genes"].append(gene_symbol)
            if species not in self.diseases[omim_id]["disease_species"]:
                self.diseases[omim_id]["disease_species"].append(species)
        else:
            self.diseases[omim_id] = {
                "disease_genes": [gene_symbol],
                "disease_species": [species],

                "name": self.omim_dataset[omim_id]["name"],
                "symbol": self.omim_dataset[omim_id]["symbol"],
                "disease_synonyms": self.omim_dataset[omim_id]["disease_synonyms"],

                "name_key": self.omim_dataset[omim_id]["name"],
                "id": omim_id,
                "key": omim_id,
                "href": "http://omim.org/entry/" + omim_id.split(":")[1],
                "category": "disease"
            }

