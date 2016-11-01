/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import d3 from 'd3';

import getSpeciesColorScale from '../lib/getSpeciesColorScale';

const DEFAULT_WIDTH = 600;
const MAX_HEIGHT = 750;

class Graph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: DEFAULT_WIDTH
    };
  }

  // fetch data at start
  componentDidMount() {
    this.calcWidth();
  }

  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
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

  getNodes() {
    let colorScale = getSpeciesColorScale();
    return this.props.data.nodes.map( d => {
      d.color = colorScale(d.species);
      return d;
    });
  }

  // a la http://bl.ocks.org/mbostock/3180395
  drawGraph() {
    let width = this.state.width;
    let height = this.getHeight();
    let nodes = this.getNodes();
    let links = this.getLinks();
    if (!nodes.length || !links.length) return;

    let force = d3.layout.force()
      .size([width, height]);
    let context = this.refs.canvas.getContext('2d');
    force
      .nodes(nodes)
      .links(links)
      .linkDistance(20)
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
      // context.fillStyle = 'black';
      // nodes.forEach(function(d) {
      //   context.fillText(d.name, d.x + TEXT_OFFSET, d.y - TEXT_OFFSET);
      // });
      // draw nodes
      nodes.forEach(function(d) {
        context.beginPath();
        context.fillStyle = d.color;
        context.moveTo(d.x, d.y);
        context.arc(d.x, d.y, 4.5, 0, 2 * Math.PI);
        context.fill();
      });
      
    }
  }

  render() {
    return (
      <div ref='container'>
        <canvas height={this.getHeight()} ref='canvas' width={this.state.width} />
      </div>
    );
  }
}

Graph.propTypes = {
  data: React.PropTypes.object // { nodes: [], edges: [] }
};

export default Graph;
