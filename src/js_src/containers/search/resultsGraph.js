/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { createMemoryHistory } from 'react-router';
import d3 from 'd3';

import { selectGraphData, selectQueryParams } from '../../selectors/searchSelectors';
import fetchData from '../../lib/fetchData';
import { receiveGraphResponse, setError, setPending } from './searchActions';
import { SEARCH_API_ERROR_MESSAGE } from '../../constants';

const BASE_SEARCH_URL = '/api/graph_search';
const DEFAULT_WIDTH = 600;
const MAX_HEIGHT = 450;
const TEXT_OFFSET = 3;

class ResultsGraphComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: DEFAULT_WIDTH
    };
  }

  // fetch data at start
  componentDidMount() {
    this.calcWidth();
    this.fetchData();
  }

  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.queryParams !== this.props.queryParams) {
      this.fetchData();
    }
    if (prevProps.data !== this.props.data) {
      this.drawGraph();
    }
  }

  calcWidth() {
    let newWidth = this.refs.container.getBoundingClientRect().width;
    this.setState({ width: newWidth });
  }

  getHeight() {
    return Math.min(this.state.width, MAX_HEIGHT);
  }

  getLinks() {
    let nodes = this.props.data.nodes;
    let edges = this.props.data.edges;
    function findIndexOfNodeById(id) {
      let thisNode = nodes.filter( d => d.id === id )[0];
      return nodes.indexOf(thisNode);
    }
    return edges.map( d => {
      let sourceIndex = findIndexOfNodeById(d.source);
      let targetIndex = findIndexOfNodeById(d.target);
      return { source: sourceIndex, target: targetIndex };
    });
  }

  // a la http://bl.ocks.org/mbostock/3180395
  drawGraph() {
    let width = this.state.width;
    let height = this.getHeight();
    let nodes = this.props.data.nodes;
    let links = this.getLinks();
    if (!nodes.length || !links.length) return;

    let force = d3.layout.force()
      .size([width, height]);
    let context = this.refs.canvas.getContext('2d');
    force
      .nodes(nodes)
      .links(links)
      .linkDistance(50)
      .on('tick', tick)
      .start();
    // setup font
    context.font = '14px Lato';
    function tick() {
      context.clearRect(0, 0, width, height);
      // draw links
      context.strokeStyle = '#ccc';
      context.beginPath();
      links.forEach(function(d) {
        context.moveTo(d.source.x, d.source.y);
        context.lineTo(d.target.x, d.target.y);
      });
      context.stroke();
      context.fillStyle = 'black';
      nodes.forEach(function(d) {
        context.fillText(d.name, d.x + TEXT_OFFSET, d.y - TEXT_OFFSET);
      });
      // draw nodes
      context.fillStyle = 'steelblue';
      context.beginPath();
      nodes.forEach(function(d) {
        context.moveTo(d.x, d.y);
        context.arc(d.x, d.y, 4.5, 0, 2 * Math.PI);
      });
      context.fill();
    }
  }

  fetchData() {
    let tempHistory = createMemoryHistory('/');
    let graphSearchUrl = tempHistory.createPath({ pathname: BASE_SEARCH_URL, query: this.props.queryParams });
    this.props.dispatch(setPending(true));
    fetchData(graphSearchUrl)
      .then( (data) => {
        this.props.dispatch(receiveGraphResponse(data));
        this.props.dispatch(setError(false));
        this.props.dispatch(setPending(false));
      })
      .catch( (e) => {
        this.props.dispatch(setPending(false));
        if (process.env.NODE_ENV === 'production') {
          this.props.dispatch(setError(SEARCH_API_ERROR_MESSAGE));
        } else {
          throw(e);
        }
      });
  }

  render() {
    return (
      <div ref='container'>
        <canvas height={this.getHeight()} ref='canvas' width={this.state.width} />
      </div>
    );
  }
}

ResultsGraphComponent.propTypes = {
  data: React.PropTypes.object, // { nodes: [], edges: [] }
  dispatch: React.PropTypes.func,
  queryParams: React.PropTypes.object
};

function mapStateToProps(state) {
  return {
    data: selectGraphData(state),
    queryParams: selectQueryParams(state)
  };
}

export { ResultsGraphComponent as ResultsGraphComponent };
export default connect(mapStateToProps)(ResultsGraphComponent);
