class DoAnnotator:

    # get the gene, disease_dataset in bulk, do_dataset
    @staticmethod
    def attach_annotations(gene, disease_dataset, do_dataset):
        gene_id = gene['primaryId']
        gene_object_id = disease_dataset[]

        if gene_id in disease_dataset:
            for do_id in disease_dataset[gene_object_id['do_id']]:
                gene.add_disease_annotation_to_gene(gene_object_id, do_id, do_dataset)

                gene["diseases"].append({
                    "do_id": do_id,
                    # in the disease map for this gene, get me the associationType, add in the do_name and give me the evidence dictionary
                    "do_name": do_dataset[do_id]['name'][0],
                    "associationType": disease_dataset[gene_id]['associationType'][0],
                    "evidence": disease_dataset[gene_id]['evidence']
                })
        return gene

    @staticmethod
    def add_disease_annotation(gene_object_id, do_id, do_dataset):
        if gene_object_id not in do_dataset[do_id]['do_genes']:
            do_dataset[do_id]['do_genes'].append(gene_object_id)

        return do_dataset
