import React, { Component } from 'react';

import style from './style.css';

class ResultsList extends Component {
  renderRows() {
    return this.props.entries.map( (d, i) => {
      return (
        <div className={style.resultContainer} key={`sr${i}`} >
          <h3>
            <a href='#'>{d.symbol}</a>
          </h3>
          <dl>
            <dt>Name:</dt>
            <dd>{d.name}</dd>
            <dt>Synonym:</dt>
            <dd>{d.synonyms}</dd>
            <dt>Source:</dt>
            <dd><a href={d.sourceHref} target='_new'>{d.geneId}</a></dd>
            <dt>Species:</dt>
            <dd><i>{d.species}</i></dd>
            <dt>Gene Type:</dt>
            <dd>{d.geneType}</dd>
            <dt>Description:</dt>
            <dd dangerouslySetInnerHTML={{ __html: d.description }} />
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
