import React, { Component } from 'react';

import style from './style.css';
import DetailList from './detailList';
import { makeFieldDisplayName } from '../../lib/searchHelpers';

const MATCH_LABEL = 'match_by';
const MAX_CHAR = 100;

class ResultsTable extends Component {
  getFields() {
    let fields;
    switch(this.props.activeCategory) {
    case 'gene':
      fields = ['display_name', 'name', 'synonyms', 'source', 'species', 'gene_type', 'genomic_coordinates', 'relative_coordinates'];
      break;
    case 'go':
      fields = ['display_name', 'synonyms', 'go_branch'];
      break;
    case 'disease':
      fields = ['display_name', 'omim_id', 'synonyms'];
      break;
    default:
      fields = ['display_name', 'synonyms'];
    }
    fields.push(MATCH_LABEL);
    return fields;
  }

  renderHeader() {
    let fields = this.getFields();
    let nodes = fields.map( (d) => {
      let processedName;
      if (this.props.activeCategory === 'gene' && d === 'display_name') {
        processedName = 'symbol';
      } else if (d === 'display_name') {
        processedName = 'name';
      } else {
        processedName = d;
      }
      return <th className={style.tableHeadCell} key={`srH.${d}`}>{makeFieldDisplayName(processedName)}</th>;
    });
    return (
      <tr>
        {nodes}
      </tr>
    );
  }

  renderTruncatedContent(original) {
    original = original || '';
    if (Array.isArray(original)) {
      original = original.join(', ');
    }
    if (original.length > MAX_CHAR) {
      return original.slice(0, MAX_CHAR) + '...';
    } else {
      return original;
    }
  }

  renderRows() {
    let fields = this.getFields();
    return this.props.entries.map( (d, i) => {
      let nodes = fields.map( (field) => {
        let _key = `srtc.${i}.${field}`;
        switch(field) {
        case 'display_name':
        case 'symbol':
          return <td key={_key}><a dangerouslySetInnerHTML={{ __html: d[field] }} href={d.href} target='_new' /></td>;
        case 'source':
          return <td key={_key}><a dangerouslySetInnerHTML={{ __html: d.gene_id }} href={d.href} target='_new' /></td>;
        case MATCH_LABEL:
          return <td key={_key}>{this.renderHighlight(d.highlight)}</td>;
        case 'species':
          return <td key={_key}><i dangerouslySetInnerHTML={{ __html: d.species }} /></td>;
        default:
          return <td dangerouslySetInnerHTML={{ __html: this.renderTruncatedContent(d[field]) }} key={_key} />;
        }        
      });
      return (
        <tr key={`tr${i}`}>
          {nodes}
        </tr>
      );
    });
  }

  renderHighlight(highlight) {
    let _data = highlight;
    let _fields = Object.keys(_data);
    return <DetailList data={_data} fields={_fields} />;
  }

  render() {
    if (this.props.activeCategory === 'none') {
      return <p>To view the results in a table, first choose a category.</p>;
    }
    return (
      <div className={style.tableContainer}>
        <table className='table'>
          <thead className='thead-default'>
            {this.renderHeader()}
          </thead>
          <tbody>
            {this.renderRows()}
          </tbody>
        </table>
      </div>
    );
  }
}

ResultsTable.propTypes = {
  activeCategory: React.PropTypes.string,
  entries: React.PropTypes.array
};

export default ResultsTable;
