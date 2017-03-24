class SoAnnotator:

	@staticmethod
    def attach_annotations(self, gene, so_dataset):
        gene['SoTermName'] = so_dataset[gene['soTermId']]['name'][0]