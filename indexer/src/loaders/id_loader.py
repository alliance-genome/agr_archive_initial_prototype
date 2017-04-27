class IdLoader:

	@staticmethod
	def process_identifiers(identifier, dataProvider):
		dataProviderDict = {
			'DRSC' : 'DRSC:'
		}

		# Remove the prefix of the identifier based on the dataProvider.
		return identifier.rsplit(dataProviderDict[dataProvider], 1)[0]

	@staticmethod
	def add_agr_prefix_by_species(identifier, species):
		speciesDict = {
			7955 : 'ZFIN:',
			6239 : 'WB:',
			10090 : '', # No MGI prefix
			10116 : '', # No RGD prefix
			559292 : 'SGD:',
			4932 : 'SGD:',
			7227 : 'FB:',
			9606 : 'HGNC:'
		}

		return speciesDict[species] + identifier
