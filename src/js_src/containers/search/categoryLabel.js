import React, { Component } from 'react';

import style from './style.css';

const CATEGORY_OPTIONS = [
  {
    name: 'all',
    displayName: 'All'
  },
  {
    name: 'gene',
    displayName: 'Genes'
  },
  {
    name: 'go',
    displayName: 'Gene Ontology'
  },
  {
    name: 'disease',
    displayName: 'Diseases'
  },
  {
    name: 'ortholog group',
    displayName: 'Ortholog Groups'
  }
];

class CategoryLabel extends Component {
  getCurrentOption() {
    let current = CATEGORY_OPTIONS.filter( d => d.name === this.props.category )[0];
    return current;
  }

  renderSprite() {
    let current = this.getCurrentOption();
    let offset = Math.max(0, CATEGORY_OPTIONS.indexOf(current)) - 1;
    let offsetStyle = `-${offset}rem`;
    return <span className={`${this.props.category} ${style.sprite}`} style={{ backgroundPositionY: offsetStyle }} />;
  }

  render() {
    let current = this.getCurrentOption();
    let label = current ? current.displayName : '';
    return <span className={style.catLabel}>{this.renderSprite()} {label}</span>;
  }
}

CategoryLabel.propTypes = {
  category: React.PropTypes.string
};

export default CategoryLabel;
