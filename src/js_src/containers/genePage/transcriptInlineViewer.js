import React, {Component} from 'react';

import style from './style.css';
// import axios from 'axios';
// import jquery from 'jquery';


class TranscriptViewer extends Component {

  constructor(props) {
    super(props);
    this.state = {imageStatus: 'loading'};
  }

  handleImageErrored() {
    this.setState({imageStatus: 'Error loading transcript preview.'});
  }

  handleImageLoaded() {
    this.setState({imageStatus: ''});
  }

  render() {
    // let jbrowsePrefx = 'http://bw.scottcain.net/jbrowse/?data=data%2F';
    let jbrowsePrefx = 'http://localhost/jbrowse/overview.html?data=data%2F';
    // location based data
    // let locationString = this.props.fmin && this.props.fmax ? this.props.chromosome + ':' + this.props.fmin + '..' + this.props.fmax : this.props.geneSymbol;
    let fmin = this.props.fmin ? this.props.fmin : 10000;
    let fmax = this.props.fmax ? this.props.fmax : 20000;
    let locationString = this.props.chromosome + ':' + fmin + '..' + fmax ;

    let jbrowseUrl = jbrowsePrefx + encodeURI(this.props.species) + '&loc=' + encodeURI(locationString) + '&tracks=All%20Genes&highlight=';

    return (
      <div>
        <iframe id="genomeFrame" className={style.jbrowse} src={jbrowseUrl} />
      </div>
    );
  }


}

TranscriptViewer.propTypes = {
  chromosome: React.PropTypes.string,
  fmax: React.PropTypes.number,
  fmin: React.PropTypes.number,
  geneSymbol: React.PropTypes.string.isRequired,
  species: React.PropTypes.string.isRequired,
};

export default TranscriptViewer;

