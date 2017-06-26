
class GoGeneAnnotLoader:

    def __init__(self, genes, go_data):
        self.go_blacklist = ("GO:0008150", "GO:0003674", "GO:0005575")
        self.go = {}
        self.genes = genes
        self.go_dataset = go_data

    def attach_annotations(self, annots):
        for annot in annots:
            self.add_go_annotation_to_gene(annot["gene_id"], annot["go_id"], annot["species"])
        return self.go

    def add_go_annotation_to_gene(self, gene_id, go_id, species):
        if go_id not in self.go_dataset or go_id in self.go_blacklist or gene_id not in self.genes:
            return

        if species == "Danio rerio":
            gene_symbol = self.genes[gene_id]["symbol"]
        else:
            gene_symbol = self.genes[gene_id]["symbol"].upper()     

        if go_id in self.go:
            if gene_symbol not in self.go[go_id]["go_genes"]:
                self.go[go_id]["go_genes"].append(gene_symbol)
            if species not in self.go[go_id]["go_species"]:
                self.go[go_id]["go_species"].append(species)
        else:
            self.go[go_id] = {
                "go_genes": [gene_symbol],
                "go_species": [species],

                "name": self.go_dataset[go_id]["name"][0],
                "description": self.go_dataset[go_id]["def"][0],
                "go_type": self.go_dataset[go_id]["namespace"][0],
                "go_synonyms": self.go_dataset[go_id].get("synonym"),

                "name_key": self.go_dataset[go_id]["name"][0],
                "id": go_id,
                "href": "http://amigo.geneontology.org/amigo/term/" + go_id,
                "category": "go"
            }
        # appends go terms to the go namespace collections on gene dictionary created in load_genes() for each mod

        go_type = self.go[go_id]["go_type"]
        term_name = self.go[go_id]["name"]

        if term_name not in self.genes[gene_id]["gene_" + go_type]:
            self.genes[gene_id]["gene_" + go_type].append(term_name)


