class IdLoader:

	@staticmethod
	def process_identifiers(identifier, dataProvider):
		dataProviderDict = {
			'DRSC' : 'DRSC:'
		}

		# Remove the prefix of the identifier based on the dataProvider.
		prefix = dataProviderDict[dataProvider]

		if identifier.startswith(prefix):
   			return identifier[len(prefix):]

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
			9606 : '' # No HGNC prefix
		}

		new_identifier = None

		if identifier:
			new_identifier = speciesDict[species] + identifier

		return new_identifier
