import React, {Component} from 'react';

import BasicGeneInfo from './basicGeneInfo';
import GenePageHeader from './genePageHeader';

const fakeGeneData = {
  primaryId: 'FBgn0000490',
  name: 'decapentaplegic',
  species: {
    taxonId: '7227',
    name: 'D. melanogaster'
  },
  symbol: 'dpp',
  geneSynopsis: 'Decapentaplegic is a ligand of the transforming growth factor-β signaling pathway that signals through Smad transcription factors. Dpp acts as a morphogen that contributes to growth regulation, patterning and stem cell fate.',
  soTermId: 'SO:0001217',
  synonyms: [
    'Tegula',
    'DPP-C',
    'blink',
    'blk',
    'heldout'
  ],
  geneLiteratureUrl: 'http://www.google.com',
  crossReferences: [
    {
      dataSource: 'NCBI',
      id: '33432'
    },
    {
      dataSource: 'UniProtKB',
      id: 'P07713'
    }
  ],
  secondaryIds: [
    'CG9885'
  ],
  metaData: {
    dateProduced: '2017-01-26T15:00:42-05:00',
    dataProvider: 'FB',
    release: 'FB2016_05'
  }
};

class GenePage extends Component {
  render() {
    return (
      <div className='container'>
        <span className='tag tag-danger'>Hardcoded data</span>
        <GenePageHeader symbol={fakeGeneData.symbol} />

        <span className='tag tag-danger'>Hardcoded data</span>
        <BasicGeneInfo geneData={fakeGeneData} />
      </div>
    );
  }
}

export default GenePage;
