/*eslint-disable react/no-set-state */
import React, { Component } from 'react';
import d3 from 'd3';

import getSpeciesColorScale from '../lib/getSpeciesColorScale';

const BAND_SIZE = 14;

class ChordDiagram extends Component {
  constructor(props) {
    super(props);
    this.state = {
      DOMSize: null
    };
  }

  componentDidMount() {
    this._calculateDOMSize();
  }

  componentDidUpdate() {
    this._renderSVG();
  }

  _calculateDOMSize () {
    let rect = this.refs.target.getBoundingClientRect();
    let size = Math.min(rect.width, rect.height);
    this.setState({ DOMSize: size });
  }

  _findNodeById(id) {
    for (let i = this.props.data.nodes.length - 1; i >= 0; i--) {
      let thisNode = this.props.data.nodes[i];
      if (thisNode.id === id) return thisNode;
    }
    return null;
  }

  getChromData() {
    if (!this.props.data) return null;
    let data = this.props.data.meta;
    if (!data) return [];
    return data.map( d => {
      return { name: d.name, length: d3.sum(d.chromosomes) };
    });
  }

  _renderSVG () {
    let colorScale = getSpeciesColorScale();
    let size = this.state.DOMSize;
    if (!size) return;
    let cData = this.getChromData();
    // create layout functions
    let diameter = size,
      radius = diameter / 2,
      innerRadius = radius - BAND_SIZE;
    const arc = d3.svg.arc()
      .outerRadius(radius)
      .innerRadius(innerRadius);
    const pie = d3.layout.pie()
      .padAngle(0.005)
      .sort(null)
      .value( d => d.length );
    let nodeTarget = d3.select(this.refs.nodeTarget);
    let chromArc = nodeTarget.selectAll('.chromArc')
      .data(pie(cData));
    chromArc.enter().append('path')
      .attr({
        class: 'chromArc',
      });
    chromArc.exit().remove();
    chromArc.attr({
      d: arc,
      fill: ( d => colorScale(d.data.name) )
    });

    let cluster = d3.layout.cluster()
      .separation( (a, b) => {
        return Math.abs(a.angle - b.angle);
      })
      .size([593, innerRadius - 15])
      .sort(function(a, b){
        return d3.ascending(a.angle, b.angle);
      });

    let bundle = d3.layout.bundle();
    let line = d3.svg.line.radial()
      .interpolate('bundle')
      .tension(0.85)
      .radius(function(d) { return d.y; })
      .angle(function(d) { return (d.x / 180 - 0.825) * Math.PI; });
    let nodeData = this.getNodes()
      .sort(function(a, b){
        return d3.ascending(a.angle, b.angle);
      });
    // prepare data
    let nodesData = cluster.nodes({ name: '', children: nodeData });

    let links = this._packageEdges();
    // d3 DOM rendering
    let filteredNodesData = nodesData.filter(function(n) { return !n.children; });
    let node = nodeTarget.selectAll('.c-node')
      .data(filteredNodesData, ( d => d.name ));
    node.exit().remove();
    node
      .enter().append('rect')
      .attr('class', 'c-node');
    node.transition()
      .attr({
        width: 4,
        height: 4,
        fill: ( d => colorScale(d.species)),
        transform: function(d) {
          return 'rotate(' + (d.x + 122) + ')translate(' + (d.y + 8) + ',0)' + (d.x < 180 ? '' : 'rotate(180)');
        }
      });
    let link = nodeTarget.selectAll('.link-node')
      .data(bundle(links));
    link.enter().append('path')
      .attr({
        'class': 'link-node',
        fill: 'none',
        stroke: '#e2e2e2',
        'stroke-dasharray': `${size} ${size}`,
        'stroke-dashoffset': size,
        d: line
      });
    link.exit().remove();
    link.transition().duration(1000)
      .attr({
        'stroke-dasharray': `${size} 0`,
        'stroke-dashoffset': 0,
        d: line
      });
  }

  // add an angle
  getNodes() {
    let chromData = this.getChromData();
    if (!chromData.length) return [];
    let genomes = this.getChromData().reduce( (prev, current, i) => {
      let prevLength = 0;
      if (prev.length) {
        let prevItem = prev[i - 1];
        prevLength = prevItem.previousLength + prevItem.length;
      }
      let newItem = current;
      newItem.previousLength = prevLength;
      prev.push(current);
      return prev;
    }, []);
    let last = genomes[genomes.length - 1];
    let maxLength = last.length + last.previousLength;
    let angleScale = d3.scale.linear()
      .domain([0, maxLength])
      .range([0, Math.PI]);
    return this.props.data.nodes.map( d => {
      let chrom = genomes.filter( _d => _d.name === d.species )[0];
      let totalChord = chrom.previousLength + d.start;
      d.angle = angleScale(totalChord);
      return d;
    });
  }

  _packageEdges() {
    return this.props.data.edges.map( (d) => {
      return { source: this._findNodeById(d.source), target: this._findNodeById(d.target) };
    });
  }

  render() {
    let svgSize = this.state.DOMSize || 100;
    let halfSize = svgSize / 2;
    return (
      <div ref='target' style={{ width: '100%', height: '100%' }}>
        <svg height={svgSize} ref='svg' width={svgSize} >
          <g className='node-target' ref='nodeTarget' transform={`translate(${halfSize},${halfSize})`} />
        </svg>
      </div>
    );
  }
}

ChordDiagram.propTypes = {
  data: React.PropTypes.object // { nodes: [], edges: [] }
};

export default ChordDiagram;
