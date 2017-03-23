class SoAnnotator:

    def attach_annotations(self, genes, so_dataset):
        for key in genes:
            genes[key]["soTermName"] = so_dataset[genes[key]["soTermId"]]["name"][0]
        return genes