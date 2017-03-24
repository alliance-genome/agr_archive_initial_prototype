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
    var fmin = this.props.fmin ? this.props.fmin : 10000;
    var fmax = this.props.fmax ? this.props.fmax : 20000;
    let locationString = this.props.chromosome + ':' + fmin + '..' + fmax ;

    let jbrowseUrl = jbrowsePrefx + encodeURI(this.props.species) + '&loc=' + encodeURI(locationString) + '&tracks=DNA%2CAll%20Genes&highlight=';
    let visualizationUrl = 'http://dev.alliancegenome.org:8891/?url=';

    // original URL
    let delay = 5000;
    let pngSuffix = '&format=PNG&delay=' + delay + '&width=600&height=300&zoom=1&quality=0.7';
    let hideControlsSuffix = '&tracklist=0&nav=0&tracklabels=0&fullviewlink=0';

    let finalUrl = visualizationUrl + encodeURIComponent(jbrowseUrl.replace('DNA%2C', '') + hideControlsSuffix) + pngSuffix;
    // jbrowseUrl = 'http://localhost/jbrowse/overview.html?data=data%2FDanio%20rerio&loc=3%3A28911808..28967174&tracks=All%20Genes&highlight=';
    return (
        <iframe id="genomeFrame" className={style.jbrowse} src={jbrowseUrl} />
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

