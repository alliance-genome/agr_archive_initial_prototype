/*eslint-disable no-undef */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Sticky } from 'react-sticky';

import fetchData from '../../lib/fetchData';
import { fetchGene, fetchGeneSuccess, fetchGeneFailure } from '../../actions/genes';
import { selectGene } from '../../selectors/geneSelectors';

import style from './style.css';
import BasicGeneInfo from './basicGeneInfo';
import GenePageHeader from './genePageHeader';
import LoadingPage from '../../components/loadingPage';
import { OrthologyTable, mockOrthologData } from '../../components/orthology';
import DiseaseTable from '../../components/disease';
import Subsection from '../../components/subsection';
import HeadMetaTags from '../../components/headMetaTags';
import TranscriptInlineViewer from './transcriptInlineViewer';
import { SMALL_COL_CLASS, LARGE_COL_CLASS } from '../../constants';

class GenePage extends Component {
  componentDidMount() {
    this.props.dispatch(fetchGene());
    fetchData(`/api/gene/${this.props.params.geneId}`)
      .then(data => {
        $('body').scrollspy({ offset: -30, target: '#agrGeneMenu' });
        this.props.dispatch(fetchGeneSuccess(data));
      })
      .catch(error => this.props.dispatch(fetchGeneFailure(error)));
  }

  renderMenu() {
    return (
      <Sticky>
        <div id='agrGeneMenu'>
          <ul className={`nav flex-column" ${style.geneNavContainer}`}>
            <li className={`nav-item ${style.navItem}`}>
              <a className='nav-link' href='#basic'>Basic</a>
            </li>
            <li className={`nav-item ${style.navItem}`}>
              <a className='nav-link' href='#transcript'>Transcript Viewer</a>
            </li>
            <li className={`nav-item ${style.navItem}`}>
              <a className='nav-link' href='#orthology'>Orthology</a>
            </li>
            <li className={`nav-item ${style.navItem}`}>
              <a className='nav-link' href='#disease'>Disease Associations</a>
            </li>
          </ul>
        </div>
      </Sticky>
    );
  }

  renderBody() {
    let title = 'AGR gene page for ' + this.props.data.species + ' gene: ' + this.props.data.symbol;

    // todo, add chromosome
    let genomeLocation ;
    if(this.props.data.genomeLocations){
      if(this.props.data.genomeLocations.length==1){
        genomeLocation = this.props.data.genomeLocations[0];
      }
      else
      if(this.props.data.genomeLocations.length>1){
        // TODO: figure out the proper assembly
        for(var i in this.props.data.genomeLocations){
          let tempGenomeLocation = this.props.data.genomeLocations[i];
          if(tempGenomeLocation.start && tempGenomeLocation.end){
            genomeLocation = tempGenomeLocation;
          }
        }
      }
    }

    return (
      <div className='container' data-spy="scroll" data-target="#agrGeneMenu">
        <HeadMetaTags title={title} />
        <Sticky stickyStyle={{ background: 'white', zIndex: 1 }}>
          <GenePageHeader symbol={this.props.data.symbol} />
        </Sticky>
        <div id='basic'>
          <Subsection>
            <BasicGeneInfo geneData={this.props.data} />
          </Subsection>
        </div>

        <div id='transcript'>
          <Subsection title='Transcript Viewer'>
            {genomeLocation && genomeLocation.start && genomeLocation.end
              ?
              <TranscriptInlineViewer
                chromosome={genomeLocation.chromosome}
                fmax={genomeLocation.end}
                fmin={genomeLocation.start}
                geneSymbol={this.props.data.symbol}
                species={this.props.data.species}
              />
              :
              <div className="alert alert-warning">Genome Location Data Unavailable</div>
            }
          </Subsection>
        </div>

        <br />

        {/*<Subsection title='Transcript Viewer'>*/}
          {/*{genomeLocation*/}
            {/*?*/}
            {/*<TranscriptViewer geneSymbol={this.props.data.symbol} species={this.props.data.species} fmin={genomeLocation.fmin } fmax={genomeLocation.fmax} chromosome={genomeLocation.chromosome}/>*/}
            {/*:*/}
            {/*<div className="alert alert-warning">Genome Location Data Unavailable</div>*/}
          {/*}*/}
        {/*</Subsection>*/}
        <div id='orthology'>
          <Subsection hardcoded title='Orthology'>
            <OrthologyTable data={mockOrthologData} />
          </Subsection>
        </div>
        <div id='disease'>
          <Subsection hardcoded title='Disease Associations'>
            <DiseaseTable />
          </Subsection>
        </div>
      </div>
    );
  }

  render() {
    if (this.props.loading) {
      return <LoadingPage />;
    }

    if (this.props.error) {
      return <div className='alert alert-danger'>{this.props.error}</div>;
    }

    if (!this.props.data) {
      return null;
    }
    return (
      <div className='row'>
        <div className={SMALL_COL_CLASS}>
          {this.renderMenu()}
        </div>
        <div className={LARGE_COL_CLASS}>
          {this.renderBody()}
        </div>
      </div>
    );
  }
}

GenePage.propTypes = {
  data: React.PropTypes.object,
  dispatch: React.PropTypes.func,
  error: React.PropTypes.object,
  loading: React.PropTypes.bool,
  params: React.PropTypes.object,
};

function mapStateToProps(state) {
  return selectGene(state);
}

export { GenePage as GenePage };
export default connect(mapStateToProps)(GenePage);
