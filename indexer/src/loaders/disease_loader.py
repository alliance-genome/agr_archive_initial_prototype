from files import *
from mods import MOD

import re


class DiseaseLoader:
    def get_data(self, disease_data):

        disease_annots = {}
        list_to_yield = []

        dateProduced = disease_data['metaData']['dateProduced']

        release = None

        if 'release' in disease_data['metaData']:
            release = disease_data['metaData']['release']

        for diseaseRecord in disease_data['data']:
            #experimentalConditions = []
            objectRelationMap = {}
            evidenceList = []
            #geneticModifiers = []
            #experimentalConditionsText = []
            inferredFromGeneAssociations = []
            modifier = {}

            # if 'experimentalConditions' in diseaseRecord:
            #     for experimentalCondition in diseaseRecord['experimentalConditions']:
            #         experimentalConditions.append({"zecoId": experimentalCondition.get('zecoId'),
            #                                        "geneOntologyId": experimentalCondition.get('geneOntologyId'),
            #                                        "ncbiTaxonId": experimentalCondition.get('ncbiTaxonID'),
            #                                        "chebiOntologyId": experimentalCondition.get('chebiOntologyId'),
            #                                        "anatomicalId": experimentalCondition.get('anatomicalId'),
            #                                        "experimentalConditionIsStandard": experimentalCondition.get('conditiionIsStandard'),
            #                                        "freeTextCondition": experimentalCondition.get('textCondition')})
            if 'evidence' in diseaseRecord:
                for evidence in diseaseRecord['evidence']:
                    evidenceCode = evidence.get('evidenceCode')
                    pubs = []
                    for pub in evidence['publications']:
                        pubMedId = pub.get('pubMedId')
                        publicationModId = pub.get('publicationModId')
                        # print pubMedId
                        # print publicationModId
                        # print diseaseRecord['evidence']
                        pubs.append({'pubMedId': pubMedId, 'publicationModId': publicationModId})
                        # print pubs
                    evidenceList.append({"pubs": pubs, "evidenceCode": evidenceCode})

            if 'objectRelation' in diseaseRecord:
                diseaseObjectType = diseaseRecord['objectRelation'].get("objectType")
                diseaseAssociationType = diseaseRecord['objectRelation'].get("objectRelation")
                #for gene in diseaseRecord['objectRelation']['inferredGeneAssociation']:
                #        inferredFromGeneAssociations.append(gene.get('primaryId'))
                objectRelationMap = {"diseaseObjectType": diseaseObjectType, "diseaseAssociationType": diseaseAssociationType}

            # if 'modifier' in diseaseRecord:
            #     associationType = diseaseRecord['modifier']['associationType'].get('associationType')
            #     if 'genetic' in diseaseRecord['modifier']['associationType']:
            #         geneticModifiers = diseaseRecord['modifier']['associationType'].get('genetic')
            #     if 'experimentalConditionsText' in diseaseRecord['modifier']['associationType']:
            #         experimentalConditionsText = diseaseRecord['modifier']['associationType'].get("experimentalConditionsText")
            #     modifierQualifier = diseaseRecord['modifier']['associationType'].get("qualifier")
            #     modifier.append({"associationType": associationType,
            #                      "geneticModifiers": geneticModifiers,
            #                      "experimentalConditionsText": experimentalConditionsText,
            #                      "modifierQualifier": modifierQualifier})

            disease_annots[diseaseRecord.get('objectId')] = {
                "diseaseObjectId": diseaseRecord.get('objectId'),
                #"diseaseObjectName": diseaseRecord.get('objectName'),
                #"qualifier": diseaseRecord.get('qualifier'),
                #"with": diseaseRecord.get('with'),
                #"taxonId": diseaseRecord.get('taxonId'),
                #"geneticSex": diseaseRecord.get('geneticSex'),
                #"dataAssigned": diseaseRecord.get('dateAssigned'),
                #"experimentalConditions": experimentalConditions,
                "associationType": diseaseRecord.get('objectRelation').get('associationType'),
                #"diseaseObjectType": diseaseRecord.get('objectRelation').get('objectType'),
                #"evidenceList": evidenceList,
                #"modifier": modifier,
                "objectRelation": objectRelationMap,
                "evidence": evidenceList,
                "do_id": diseaseRecord.get('DOid'),
                "do_name": None
              }

        return disease_annots
