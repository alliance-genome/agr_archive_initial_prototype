def check_for_test_entry(primary_id):
    test_set = {'HGNC:17889', 'HGNC:25818', 'HGNC:3686',
                'RGD:70891', 'RGD:1306349', 'RGD:620796',
                'MGI:109337', 'MGI:108202', 'MGI:2676586',
                'ZDB-GENE-990415-72', 'ZDB-GENE-030131-3445', 'ZDB-GENE-980526-388'
                'FBgn0083973', 'FBgn0037960', 'FBgn0027296',
                'WBGene00044305', 'WBGene00169423', 'WBGene00000987',
                'S000003256', 'S000003513', 'S000000119'}

    if primary_id in test_set:
        return 'true'
    else:
        return 'false'