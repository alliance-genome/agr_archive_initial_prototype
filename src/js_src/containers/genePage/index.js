import React, { Component } from 'react';
import { OrthologyTable } from '../../components/orthology';
import { connect } from 'react-redux';

import fetchData from '../../lib/fetchData';
import { fetchGene, fetchGeneSuccess, fetchGeneFailure } from '../../actions/genes';
import { selectGene } from '../../selectors/geneSelectors';

import BasicGeneInfo from './basicGeneInfo';
import GenePageHeader from './genePageHeader';

const mockOrthologData = [
  {
    species: 'Homo sapiens',
    geneSymbol: 'GAK',
    geneURL: 'http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4113',
    ncbiID: '2580',
    scoreNumerator: 11,
    scoreDemominator: 11,
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: true},
      {id: 'inparanoid', isCalled: true},
      {id: 'isobase', isCalled: true},
      {id: 'oma', isCalled: true},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: true},
      {id: 'treefam', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: true},
      {id: 'isobase', isCalled: false},
      {id: 'oma', isCalled: false},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: true},
      {id: 'inparanoid', isCalled: true},
      {id: 'isobase', isCalled: true},
      {id: 'oma', isCalled: true},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: true},
      {id: 'treefam', isCalled: true},
      {id: 'zfin', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: true},
      {id: 'isobase', isCalled: false},
      {id: 'oma', isCalled: false},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: true},
      {id: 'zfin', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: true},
      {id: 'inparanoid', isCalled: false},
      {id: 'oma', isCalled: true},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: false},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: true},
      {id: 'zfin', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: true},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: true},
      {id: 'oma', isCalled: false},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: false},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: false},
      {id: 'zfin', isCalled: false},
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
    methods: [
      {id: 'compara', isCalled: false},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: false},
      {id: 'isobase', isCalled: true},
      {id: 'oma', isCalled: false},
      {id: 'orthodb', isCalled: true},
      {id: 'orthomcl', isCalled: true},
      {id: 'panther', isCalled: false},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: true},
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
    methods: [
      {id: 'compara', isCalled: false},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: false},
      {id: 'isobase', isCalled: false},
      {id: 'oma', isCalled: false},
      {id: 'orthodb', isCalled: false},
      {id: 'orthomcl', isCalled: false},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: false},
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
    methods: [
      {id: 'compara', isCalled: false},
      {id: 'homologene', isCalled: false},
      {id: 'inparanoid', isCalled: false},
      {id: 'isobase', isCalled: false},
      {id: 'oma', isCalled: false},
      {id: 'orthomcl', isCalled: false},
      {id: 'panther', isCalled: true},
      {id: 'phylome', isCalled: true},
      {id: 'roundup', isCalled: false},
      {id: 'treefam', isCalled: false},
    ],
    isBestScore: true,
    isBestScoreReverse: true,
    alignURL: null,
  }
];


class GenePage extends Component {
  componentDidMount() {
    this.props.dispatch(fetchGene());
    fetchData(`/api/gene/${this.props.params.geneId}`)
      .then(data => this.props.dispatch(fetchGeneSuccess(data)))
      .catch(error => this.props.dispatch(fetchGeneFailure(error)));
  }

  render() {
    if (this.props.loading) {
      return <span>loading...</span>;
    }

    if (this.props.error) {
      return <div className='alert alert-danger'>{this.props.error}</div>;
    }

    if (!this.props.data) {
      return null;
    }

    return (
      <div className='container'>
        <GenePageHeader symbol={this.props.data.symbol} />
        <BasicGeneInfo geneData={this.props.data} />
        <OrthologyTable data={mockOrthologData} />
      </div>
    );
  }
}

GenePage.propTypes = {
  data: React.PropTypes.object,
  dispatch: React.PropTypes.func,
  error: React.PropTypes.object,
  loading: React.PropTypes.bool,
  params: React.PropTypes.object,
};

function mapStateToProps(state) {
  return selectGene(state);
}

export { GenePage as GenePage };
export default connect(mapStateToProps)(GenePage);
