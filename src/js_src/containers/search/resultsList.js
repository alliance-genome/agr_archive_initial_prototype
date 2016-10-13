import React, { Component } from 'react';

import style from './style.css';
import CategoryLabel from './categoryLabel';
import DetailList from './detailList';

const DEFAULT_FIELDS = ['symbol', 'gene_symbol', 'name', 'gene_synonyms', 'synonyms', 'sourceHref', 'geneId', 'species', 'type'];

class ResultsList extends Component {
  renderHighlightedValues(highlight) {
    let _data = highlight;
    let _fields = Object.keys(_data).filter( d => {
      return (DEFAULT_FIELDS.indexOf(d) < 0);
    });
    return <DetailList data={_data} fields={_fields} />;
  }

  renderHeader(d) {
    return (
      <div>
        <span className={style.resultCatLabel}>Category: <CategoryLabel category={d.category} /></span>
        <h4>
          <a dangerouslySetInnerHTML={{ __html: d.displayName }} href={d.href} target='_new' />
        </h4>
      </div>
    );
  }

  renderDetailFromFields(d, fields) {
    return <DetailList data={d} fields={fields} />;
  }

  renderDiseaseEntry(d, i) {
    let fields = ['synonyms', 'omim_id'];
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
        {this.renderDetailFromFields(d, fields)}
        <hr />
      </div>
    );
  }

  renderGeneEntry(d, i) {
    let topFields = ['name', 'synonyms'];
    let bottomFields = ['species', 'geneType'];
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
          {this.renderDetailFromFields(d, topFields)}
          <div className={style.detailContainer}>
            <span className={style.detailLabel}><strong>Source:</strong> </span>
            <span><a dangerouslySetInnerHTML={{ __html: d.geneId }} href={d.sourceHref} target='_new' /></span>
          </div>
          {this.renderDetailFromFields(d, bottomFields)}
          {this.renderHighlightedValues(d.highlight)}
        <hr />
      </div>
    );
  }

  renderGoEntry(d, i) {
    let fields = ['synonyms', 'go_branch'];
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
        {this.renderDetailFromFields(d, fields)}
        <hr />
      </div>
    );
  }

  renderOrthologGroupEntry(d, i) {
    let fields = ['associated_genes'];
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
        {this.renderDetailFromFields(d, fields)}
        <hr />
      </div>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      switch(d.category) {
      case 'ortholog group':
        return this.renderOrthologGroupEntry(d, i);
      case 'disease':
        return this.renderDiseaseEntry(d, i);
      case 'gene':
        return this.renderGeneEntry(d, i);
      case 'go':
        return this.renderGoEntry(d, i);
      default:
        return this.renderGeneEntry(d, i);
      }
    });
  }

  render() {
    return (
      <div>
        {this.renderRows()}
      </div>
    );
  }
}

ResultsList.propTypes = {
  entries: React.PropTypes.array
};

export default ResultsList;
