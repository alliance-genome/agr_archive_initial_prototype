import React, {Component} from 'react';

import DataSourceCard from './dataSourceCard';

class BasicGeneInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      geneData: this.props.geneData,
      speciesData: {
        species: this.props.geneData.species.name,
        dataProvider: this.props.geneData.metaData.dataProvider,
        primaryId: this.props.geneData.primaryId,
      }
    };
  }

  render() {
    return (
      <div className='row'>
        <div className='col-sm-4 push-sm-8'>
          <DataSourceCard sourceData={this.state.speciesData} />
        </div>
        <div className='col-sm-8 pull-sm-4'>
          <dl className='row'>
            <dt className='col-sm-2'>Symbol</dt>
            <dd className='col-sm-10'>{this.state.geneData.symbol}</dd>

            <dt className='col-sm-2'>Name</dt>
            <dd className='col-sm-10'>{this.state.geneData.name}</dd>

            <dt className='col-sm-2'>Synonyms</dt>
            <dd className='col-sm-10'>{this.state.geneData.synonyms.join(', ')}</dd>

            <dt className='col-sm-2'>Biotype</dt>
            <dd className='col-sm-10'>{this.state.geneData.soTermId}</dd>

            <dt className='col-sm-2'>Description</dt>
            <dd className='col-sm-10'>{this.state.geneData.geneSynopsis}</dd>

            <dt className='col-sm-2'>Genomic Resources</dt>
            <dd className='col-sm-10'>
              {this.state.geneData.crossReferences.map((ref, idx) => {
                return <div key={`ref-${idx}`}>{ref.dataSource}: <a href='#'>{ref.id}</a></div>;
              })}
            </dd>

            <dt className='col-sm-2'>Additional Information</dt>
            <dd className='col-sm-10'><a href={this.state.geneData.geneLiteratureUrl}>Literature</a></dd>
          </dl>
        </div>
      </div>
    );
  }
}

BasicGeneInfo.propTypes = {
  geneData: React.PropTypes.object
};

export default BasicGeneInfo;
