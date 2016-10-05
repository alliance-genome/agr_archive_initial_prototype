import React, { Component } from 'react';

import style from './style.css';
import { makeFieldDisplayName } from '../../lib/searchHelpers';

const DEFAULT_FIELDS = ['name', 'synonym', 'sourceHref', 'geneId', 'species', 'type'];

class ResultsList extends Component {
  renderHighlightedValues(highlight) {
    let displayedVals = Object.keys(highlight).filter( d => {
      return (DEFAULT_FIELDS.indexOf(d) < 0);
    });

    let nodes = displayedVals.map( d => {
      return (
        <div key={`srHigh.${d}`}>
          <dt>{makeFieldDisplayName(d)}:</dt>
          <dd dangerouslySetInnerHTML={{ __html: highlight[d] }} />
        </div>
      );
    });
    return (
      <div>
        {nodes}
      </div>
    );
  }

  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <div className={style.resultContainer} key={`sr${i}`} >
          <h3>
            <a dangerouslySetInnerHTML={{ __html: d.symbol }} href='#' />
          </h3>
          <dl className={style.detailList}>
            <dt>Name:</dt>
            <dd dangerouslySetInnerHTML={{ __html: d.name }} />
            <dt>Synonym:</dt>
            <dd dangerouslySetInnerHTML={{ __html: d.synonym }} />
            <dt>Source:</dt>
            <dd><a dangerouslySetInnerHTML={{ __html: d.geneId }} href={d.sourceHref} target='_new' /></dd>
            <dt>Species:</dt>
            <dd><i dangerouslySetInnerHTML={{ __html: d.species }} /></dd>
            <dt>Gene Type:</dt>
            <dd dangerouslySetInnerHTML={{ __html: d.geneType }} />
            {this.renderHighlightedValues(d.highlight)}
          </dl>
          <hr />
        </div>
      );
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
