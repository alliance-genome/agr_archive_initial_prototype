import React, { Component } from 'react';

import style from './style.css';
import CategoryLabel from './categoryLabel';
import DetailList from './detailList';

const DEFAULT_FIELDS = ['symbol', 'gene_symbol', 'name', 'gene_synonyms', 'synonyms', 'sourceHref', 'gene_id', 'species', 'type'];

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
        <span className={style.resultCatLabel}><CategoryLabel category={d.category} /></span>
        <h4>
          <a dangerouslySetInnerHTML={{ __html: d.display_name }} href={d.href} target='_new' />
        </h4>
      </div>
    );
  }

  renderDetailFromFields(d, fields) {
    return <DetailList data={d} fields={fields} />;
  }

  renderNonGeneEntry(d, i, fields) {
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
        {this.renderDetailFromFields(d, fields)}
        {this.renderHighlightedValues(d.highlight)}
        <hr />
      </div>
    );
  }

  renderOrthologs(orthologs, label) {
    label = label || 'Orthologs';
    if (orthologs.length === 0) return null;
    let nodes = orthologs.map( (d, i) => {
      let commaNode = (i === orthologs.length - 1) ? null : ', ';
      let evidenceNodes = d.evidences.map( (_d, _i) => {
        let commaNode = (_i === d.evidences.length - 1) ? null : ', ';
        return <span className={style.evidenceFootnote} key={`oe.${i}.${_i}`}>{_d.name}{commaNode}</span>;
      });
      return (
        <span key={'ortho.' + i}>
          <a href={d.href} target='_new'>{d.symbol}</a> {evidenceNodes}{commaNode}
        </span>
      );
    });
    return (
      <div className={style.detailContainer}>
        <span className={style.detailLabel}><strong>{label}:</strong> {nodes}</span>
      </div>
    );
  }

  renderHomologyGroup(d, i, fields) {
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
        {this.renderDetailFromFields(d, fields)}
        {this.renderHighlightedValues(d.highlight)}
        {this.renderOrthologs(d.member_genes, 'Member Genes')}
        <hr />
      </div>
    );
  }

  renderGeneEntry(d, i) {
    let topFields = ['name', 'synonyms'];
    let bottomFields = ['species', 'gene_type'];
    return (
      <div className={style.resultContainer} key={`sr${i}`}>
        {this.renderHeader(d)}
          {this.renderDetailFromFields(d, topFields)}
          <div className={style.detailContainer}>
            <span className={style.detailLabel}><strong>Source:</strong> </span>
            <span><a dangerouslySetInnerHTML={{ __html: d.gene_id }} href={d.sourceHref} target='_new' /></span>
          </div>
          {this.renderDetailFromFields(d, bottomFields)}
          {this.renderOrthologs(d.orthologs)}
          {this.renderHighlightedValues(d.highlight)}
        <hr />
      </div>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      if (d.category === 'gene') {
        return this.renderGeneEntry(d, i);
      } else {
        let fieldVals = {
          'disease': ['synonyms', 'omim_id'],
          'go': ['synonyms', 'go_branch'],
          'homology group': ['associated_genes']
        };
        let fields = fieldVals[d.category] || [];
        return this.renderNonGeneEntry(d, i, fields);
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
