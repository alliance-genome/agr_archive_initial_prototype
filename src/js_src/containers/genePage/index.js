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
