import React, { Component } from 'react';
import HeadMetaTags from '../../components/headMetaTags';
import Subsection from '../../components/subsection';
import { DiseasePageAssociationsTable } from '../../components/disease';

class DiseasePage extends Component {
  render() {
    const title = this.props.params.diseaseId;
    return (
      <div className='container'>
        <HeadMetaTags title={title} />
        <div className='alert alert-warning'>
          <i className='fa fa-warning' /> Page under active development
        </div>
        <h1>
          {this.props.params.diseaseId}
          <hr />
        </h1>
        <a href={'http://www.disease-ontology.org/?id=' + this.props.params.diseaseId}>
          {this.props.params.diseaseId}
        </a>

        <Subsection hardcoded title='Associations'>
          <DiseasePageAssociationsTable />
        </Subsection>
      </div>
    );
  }
}

DiseasePage.propTypes = {
  params: React.PropTypes.object,
};

export default DiseasePage;
