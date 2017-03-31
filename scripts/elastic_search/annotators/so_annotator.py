class SoAnnotator:

    @staticmethod
    def attach_annotations(gene, so_dataset):
        gene['soTermName'] = so_dataset[gene['soTermId']]['name'][0]
        return gene