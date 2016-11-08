/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import d3 from 'd3';
import sigma from 'sigma';
import getSpeciesColorScale from '../lib/getSpeciesColorScale';

const MAX_HEIGHT = 450;
const TARGET_ID = 'j-agr-sigma-target';

class Graph extends Component {
  // fetch data whenever URL changes within /search
  componentDidUpdate (prevProps) {
    if (prevProps.data !== this.props.data) {
      this.drawGraph();
    }
  }

  getHeight() {
    return MAX_HEIGHT;
  }

  // the edges need by d3 to calc format
  getFormattedLinks() {
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

  getEdges() {
    let data = this.props.data;
    let rawEdges = data.edges;
    return rawEdges.map( (d, i) => {
      d.id = `e${i}`;
      d.color = '#e2e2e2';
      return d;
    });
  }

  getNodes() {
    let colorScale = getSpeciesColorScale();
    return this.props.data.nodes.map( (d) => {
      d.color = colorScale(d.species);
      d.label = d.name;
      d.size = d.direct ? 1 : 0.5;
      return d;
    });
  }

  // calc static d3 force
  getFormattedNodes() {
    let nodes = this.getNodes();
    let links = this.getFormattedLinks();
    let force = d3.layout.force()
      .size([1, 1])
      .nodes(nodes)
      .links(links)
      .linkDistance(20);
    force.start();
    let nTickets = 100;
    for (let i = 0; i <= nTickets; i++) {
      force.tick();
    }
    force.stop();
    return nodes;
  }

  drawGraph() {
    if (this.s) {
      this.s.graph.clear();
      this.s.refresh();
    }
    let _nodes = this.getFormattedNodes();
    let _edges = this.getEdges();
    if (!_nodes.length) return;
    let _graph = {
      nodes: _nodes,
      edges: _edges
    };
    this.s = new sigma({
      graph: _graph,
      container: TARGET_ID,
      settings: {
        labelThreshold: 100,
        minNodeSize: 0,
        maxNodeSize: 3,
      }
    });
  }

  render() {
    return (
      <div ref='container'>
        <div id={TARGET_ID} style={{ height: this.getHeight() }} />
      </div>
    );
  }
}

Graph.propTypes = {
  data: React.PropTypes.object // { nodes: [], edges: [] }
};

export default Graph;
