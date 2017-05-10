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
            primaryId = diseaseRecord.get('objectId')

            if 'evidence' in diseaseRecord:
                for evidence in diseaseRecord['evidence']:
                    evidenceCode = evidence.get('evidenceCode')
                    pubs = []
                    for pub in evidence['publications']:
                        pubMedId = pub.get('pubMedId')
                        if pubMedId is not None:
                            if ':' in pubMedId:
                                local_pubmedid_id = pubMedId.split(":")[1]
                        publicationModId = pub.get('modPublicationId')
                        if pubMedId is not None:
                            pubs.append({'pubMedId': pubMedId, 'publicationModId': publicationModId, 'pubMedUrl': 'https://www.ncbi.nlm.nih.gov/pubmed/' + local_pubmedid_id})
                        else:
                            pubs.append({'pubMedId': pubMedId, 'publicationModId': publicationModId})
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
