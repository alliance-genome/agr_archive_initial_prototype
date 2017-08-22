from files import *
from mods import MOD
import json
import re


class DiseaseLoader:
    def get_data(self, disease_data):

        disease_annots = {}
        list_to_yield = []

        dateProduced = disease_data['metaData']['dateProduced']
        dataProvider = disease_data['metaData']['dataProvider']
        release = None
        uniqueId = set()
        infID = ""
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


            if 'qualifier' in diseaseRecord:
                qualifier = diseaseRecord.get('qualifier')
            if 'evidence' in diseaseRecord['evidence']:
                for evidence in diseaseRecord['evidence']:
                    pub = evidence.get('publication')

                    publicationModId = pub.get('modPublicationId')
                    if publicationModId is not None:
                        localPubModId = publicationModId.split(":")[1]
                        pubModUrl= self.get_complete_pub_url(localPubModId, publicationModId)
                    if pubMedId is not None:
                        pubMedId = pub.get('pubMedId')
                        if ':' in pubMedId:
                            localPubMedId = pubMedId.split(":")[1]
                            pubMedUrl = self.get_complete_pub_url(localPubMedId, pubMedId)
                    evidenceCodes = evidence.get('evidenceCodes')
                    evidenceList.append({"pubMedId": pubMedId, "pubMedUrl": pubMedUrl, "pubModId": publicationModId, "pubModUrl": pubModUrl, "evidenceCodes": evidenceCodes})

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
            # if 'modifier' in diseaseRecord:
            #     associationType = diseaseRecord['modifier']['associationType']
            #     if 'genetic' in diseaseRecord['modifier']:
            #         for geneticModifier in diseaseRecord['modifier'].get('genetic'):
            #             geneticModifier.append(diseaseRecord['modifier'].get('genetic'))
            #     if 'experimentalConditionsText' in diseaseRecord['modifier']:
            #         experimentalConditionsText = diseaseRecord['modifier'].get('experimentalConditionsText')
            #
            #     #modifierQualifier = diseaseRecord['qualifier']
            #     modifier = {"associationType": associationType,
            #                 "geneticModifiers": geneticModifiers,
            #                 "experimentalConditionsText": experimentalConditionsText#,
            #                 #"modifierQualifier": modifierQualifier
            #                 }

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
                    "evidenceList": evidenceList,
                    #"modifier": modifier,
                    #"objectRelation": objectRelationMap,
                    "evidence": evidenceList,
                    "do_id": diseaseRecord.get('DOid'),
                    "do_name": None,
                    "dateProduced": dateProduced,
                    "release": release,
                    "dataProvider": dataProvider,
                    "doIdDisplay": {"displayId": diseaseRecord.get('DOid'), "url": "http://www.disease-ontology.org/?id=" + diseaseRecord.get('DOid'), "prefix": "DOID"}
                })

                # if 'objectRelation' in diseaseRecord:
                #     if 'inferredFromID' in diseaseRecord['objectRelation']:
                #         infID = diseaseRecord['objectRelation'].get('inferredFromID');
                # else:
                #     infID = "sierra"
                # if primaryId == 'MGI:107717':
                #     print json.dumps(disease_annots[primaryId], indent=4)
                #     print primaryId + diseaseRecord.get('dateAssigned') + diseaseRecord.get('objectRelation').get(
                #         'associationType') + infID + diseaseRecord.get('DOid') + diseaseRecord.get('taxonId').join(
                #         str(p) for p in evidenceList)
                #     stuff = primaryId + diseaseRecord.get('objectRelation').get(
                #         'associationType') + infID + diseaseRecord.get('DOid') + diseaseRecord.get('taxonId').join(
                #         str(p) for p in evidenceList)
                    # if stuff in uniqueId:
                    #     print "sierra"
                    # else:
                    #     uniqueId.add(stuff)
        #for thing in uniqueId:
        #    print thing;
        #print json.dumps(disease_annots['MGI:107717'], indent=4)


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
        if 'PUBMED:' in global_id:
            complete_url = 'https://www.ncbi.nlm.nih.gov/pubmed/' + local_id


        return complete_url
