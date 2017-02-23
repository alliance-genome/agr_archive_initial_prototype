import React, { Component } from 'react';

import style from './style.css';

const ZEBRAFISH = 'Danio rerio';

class JBrowse extends Component {
  render() {
    let jbrowseUrl = 'http://bw.scottcain.net/jbrowse/';
    jbrowseUrl += '?data=' + encodeURIComponent('data/' + this.props.species);
    jbrowseUrl += '&loc=' + encodeURIComponent(this.props.geneSymbol);
    let tracks = (this.props.species === ZEBRAFISH) ? 'Genes' : 'All Genes';
    jbrowseUrl += '&tracks=' + encodeURIComponent(tracks);
    jbrowseUrl += '&nav=0&overview=0&tracklist=0';

    return (
      <iframe className={style.jbrowse} src={jbrowseUrl} />
    );
  }
}

JBrowse.propTypes = {
  geneSymbol: React.PropTypes.string.isRequired,
  species: React.PropTypes.string.isRequired,
};

export default JBrowse;
