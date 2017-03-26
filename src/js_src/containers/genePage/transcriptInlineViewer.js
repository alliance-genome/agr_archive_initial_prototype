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
    let visualizationUrl = 'http://dev.alliancegenome.org:8891/?url=';
    let delay = 5000;
    let pngSuffix = '&format=PNG&delay=' + delay + '&width=600&height=300&zoom=1&quality=0.7';
    // location based data
    // let locationString = this.props.fmin && this.props.fmax ? this.props.chromosome + ':' + this.props.fmin + '..' + this.props.fmax : this.props.geneSymbol;
    let fmin = this.props.fmin ? this.props.fmin : 10000;
    let fmax = this.props.fmax ? this.props.fmax : 20000;
    let locationString = this.props.chromosome + ':' + fmin + '..' + fmax;

    let jbrowseUrl = jbrowsePrefx + encodeURI(this.props.species) + '&loc=' + encodeURI(locationString) + '&tracks=All%20Genes&highlight=';
    let finalUrl = visualizationUrl + encodeURIComponent(jbrowseUrl.replace('DNA%2C', '')) + pngSuffix;

    return (
      <div className={style.jbrowse}>
        <iframe id="genomeFrame" className={style.jbrowse} src={jbrowseUrl}/>
        {/*<a href={jbrowseUrl} rel="noopener noreferrer" target='_blank'>*/}
          {/*<img*/}
            {/*onError={this.handleImageErrored.bind(this)}*/}
            {/*onLoad={this.handleImageLoaded.bind(this)}*/}
            {/*src={finalUrl}*/}
          {/*/>*/}
        {/*</a>*/}
        {/*{this.state.imageStatus === 'loading'*/}
          {/*? <div>Loading ... <img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif"/></div>*/}
          {/*: ''*/}
        {/*}*/}
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

