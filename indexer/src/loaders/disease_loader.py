from files import *
from mods import MOD

import re


class DiseaseLoader:
    def get_data(self, disease_data):

        disease_annots = {}
        list_to_yield = []

        dateProduced = disease_data['metaData']['dateProduced']
        dataProvider = disease_data['metaData']['dataProvider']
        release = None

        if 'release' in disease_data['metaData']:
            release = disease_data['metaData']['release']

        for diseaseRecord in disease_data['data']:
            experimentalConditions = []
            objectRelationMap = {}
            evidenceList = []
            geneticModifiers = []
            inferredFromGeneAssociations = []
            modifier = {}
            modifierQualifier = None;
            qualifier = None;
            primaryId = diseaseRecord.get('objectId')

            if 'HGNC' in primaryId:
                primaryId = primaryId[5:]
            if 'qualifier' in diseaseRecord:
                qualifier = diseaseRecord.get('qualifier')
            if 'evidence' in diseaseRecord:
                for evidence in diseaseRecord['evidence']:
                    evidenceCode = evidence.get('evidenceCode')
                    pubs = []
                    for pub in evidence['publications']:
                        pubMedId = pub.get('pubMedId')
                        if pubMedId is not None:
                            if ':' in pubMedId:
                                localPubMedId = pubMedId.split(":")[1]
                        publicationModId = pub.get('modPublicationId')
                        if publicationModId is not None:
                            localPubModId = publicationModId.split(":")[1]
                        if pubMedId is not None:
                            pubs.append({'pubMedId': pubMedId, 'pubMedUrl': 'https://www.ncbi.nlm.nih.gov/pubmed/' + localPubMedId})
                        else:
                            if publicationModId is not None:
                                pubs.append({'publicationModId': publicationModId, 'pubModUrl': self.get_complete_pub_url(localPubModId, publicationModId)})
                    evidenceList.append({"pubs": pubs, "evidenceCode": evidenceCode})

            if 'objectRelation' in diseaseRecord:
                diseaseObjectType = diseaseRecord['objectRelation'].get("objectType")
                diseaseAssociationType = diseaseRecord['objectRelation'].get("associationType")
                
                #for gene in diseaseRecord['objectRelation']['inferredGeneAssociation']:
                #        inferredFromGeneAssociations.append(gene.get('primaryId'))
                objectRelationMap = {"diseaseObjectType": diseaseObjectType, "diseaseAssociationType": diseaseAssociationType}

            if 'experimentalConditions' in diseaseRecord:
                for experimentalCondition in diseaseRecord['experimentalConditions']:
                    experimentalConditions.append({"zecoId": experimentalCondition.get('zecoId'),
                                                   "geneOntologyId": experimentalCondition.get('geneOntologyId'),
                                                   "ncbiTaxonId": experimentalCondition.get('ncbiTaxonID'),
                                                   "chebiOntologyId": experimentalCondition.get('chebiOntologyId'),
                                                   "anatomicalId": experimentalCondition.get('anatomicalId'),
                                                   "experimentalConditionIsStandard": experimentalCondition.get(
                                                       'conditiionIsStandard'),
                                                   "freeTextCondition": experimentalCondition.get('textCondition')})
            if 'modifier' in diseaseRecord:
                associationType = diseaseRecord['modifier']['associationType']
                if 'genetic' in diseaseRecord['modifier']:
                    for geneticModifier in diseaseRecord['modifier'].get('genetic'):
                        geneticModifier.append(diseaseRecord['modifier'].get('genetic'))
                if 'experimentalConditionsText' in diseaseRecord['modifier']:
                    experimentalConditionsText = diseaseRecord['modifier'].get('experimentalConditionsText')

                modifierQualifier = diseaseRecord['modifier']['qualifier']
                modifier = {"associationType": associationType,
                            "geneticModifiers": geneticModifiers,
                            "experimentalConditionsText": experimentalConditionsText,
                            "modifierQualifier": modifierQualifier}

            if primaryId not in disease_annots:
                disease_annots[primaryId] = []
            # many fields are commented out to fulfill 0.6 requirements only, but still parse the entire file.

            if modifierQualifier is None and qualifier is None:
                disease_annots[primaryId].append({
                    "diseaseObjectName": diseaseRecord.get('objectName'),
                    "qualifier": diseaseRecord.get('qualifier'),
                    "with": diseaseRecord.get('with'),
                    "taxonId": diseaseRecord.get('taxonId'),
                    "geneticSex": diseaseRecord.get('geneticSex'),
                    "dataAssigned": diseaseRecord.get('dateAssigned'),
                    "experimentalConditions": experimentalConditions,
                    "associationType": diseaseRecord.get('objectRelation').get('associationType'),
                    "diseaseObjectType": diseaseRecord.get('objectRelation').get('objectType'),
                    #"evidenceList": evidenceList,
                    "modifier": modifier,
                    #"objectRelation": objectRelationMap,
                    "evidence": evidenceList,
                    "do_id": diseaseRecord.get('DOid'),
                    "do_name": None,
                    "dateProduced": dateProduced,
                    "release": release,
                    "dataProvider": dataProvider,
                    "doIdDisplay": {"displayId": diseaseRecord.get('DOid'), "url": "http://www.disease-ontology.org/?id=" + diseaseRecord.get('DOid'), "prefix": "DOID"}
                })
        return disease_annots

    def get_complete_pub_url(self, local_id, global_id):

        complete_url = None

        if 'MGI' in global_id:
            complete_url = 'http://www.informatics.jax.org/accession/' + global_id

        if 'RGD' in global_id:
            complete_url = 'http://rgd.mcw.edu/rgdweb/search/search.html?term=' + local_id
        if 'SGD' in global_id:
            complete_url = 'http://www.yeastgenome.org/reference/' + local_id
        if 'FB' in global_id:
            complete_url = 'http://flybase.org/reports/' + local_id + '.html'
        if 'ZFIN' in global_id:
            complete_url = 'http://zfin.org/' + local_id
        if 'WB:' in global_id:
            complete_url = 'http://www.wormbase.org/db/misc/paper?name=' + local_id

        return complete_url
