import React, { Component } from 'react';
import OrthologTable from '../../components/genePage/orthologTable';


const mockOrthologData = [
  {
    species: 'Homo sapiens',
    geneSymbol: 'GAK',
    geneURL: 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4113',
    ncbiID: '2580',
    scoreNumerator: 11,
    scoreDemominator: 11,
    sources: [
      'compara',
      'homologene',
      'inparanoid',
      'isobase',
      'oma',
      'orthodb',
      'orthomcl',
      'panther',
      'phylome',
      'roundup',
      'treefam',
      'zfin'
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Homo sapiens',
    geneSymbol: 'DNAJC6',
    geneURL: 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4113',
    ncbiID: '9829',
    scoreNumerator: 7,
    scoreDemominator: 11,
    sources: [
      'compara',
      'inparanoid',
      'orthodb',
      'orthomcl',
      'panther',
      'phylome',
      'treefam'
    ],
    isBestScore: false,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Mus musculus',
    geneSymbol: 'Gak',
    geneURL: 'http://www.informatics.jax.org/marker/MGI:2442153',
    ncbiID: '231580',
    scoreNumerator: 11,
    scoreDemominator: 11,
    sources: [
      'compara',
      'homologene',
      'inparanoid',
      'isobase',
      'oma',
      'orthodb',
      'orthomcl',
      'panther',
      'phylome',
      'roundup',
      'treefam',
      'zfin'
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Mus musculus',
    geneSymbol: 'Dnajc6',
    geneURL: 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4113',
    ncbiID: '72685',
    scoreNumerator: 7,
    scoreDemominator: 11,
    sources: [
      'compara',
      'inparanoid',
      'orthodb',
      'orthomcl',
      'panther',
      'phylome',
      'treefam'
    ],
    isBestScore: false,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Danio rerio',
    geneSymbol: 'Gak',
    geneURL: 'https://zfin.org/ZDB-GENE-041210-358',
    ncbiID: '100151158',
    scoreNumerator: 7,
    scoreDemominator: 11,
    sources: [
      'compara',
      'homologene',
      'oma',
      'orthodb',
      'orthomcl',
      'panther',
      'treefam',
      'zfin'
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Danio rerio',
    geneSymbol: 'Dnajc6',
    geneURL: 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4113',
    ncbiID: '796354',
    scoreNumerator: 5,
    scoreDemominator: 11,
    sources: [
      'compara',
      'inparanoid',
      'orthodb',
      'orthomcl',
      'panther',
    ],
    isBestScore: false,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Caenorhabditis elegans',
    geneSymbol: 'tag-257',
    geneURL: 'http://www.wormbase.org/species/c_elegans/gene/WBGene00018516',
    ncbiID: '180844',
    scoreNumerator: 5,
    scoreDemominator: 11,
    sources: [
      'isobase',
      'orthodb',
      'orthomcl',
      'phylome',
      'treefam'
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Caenorhabditis elegans',
    geneSymbol: 'dnj-25',
    geneURL: 'http://www.wormbase.org/species/c_elegans/gene/WBGene00001043',
    ncbiID: '180844',
    scoreNumerator: 5,
    scoreDemominator: 11,
    sources: [
      'panther',
      'phylome'
    ],
    isBestScore: false,
    isBestScoreReverse: true,
    alignURL: null,
  },
  {
    species: 'Saccharomyces cerevisiae',
    geneSymbol: 'SWA2',
    geneURL: 'http://www.yeastgenome.org/locus/S000002728',
    ncbiID: '851918',
    scoreNumerator: 2,
    scoreDemominator: 11,
    sources: [
      'panther',
      'phylome'
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  }
];
class GenePage extends Component {
  render() {
    return (
      <div>
        <h1>GenePage</h1>
        <OrthologTable data={mockOrthologData} />
      </div>
    );
  }
}

export default GenePage;
