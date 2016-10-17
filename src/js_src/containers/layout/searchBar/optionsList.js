import React, { Component } from 'react';

import style from './style.css';

class OptionsList extends Component {
  render() {
    let options = this.props.options;
    if (options.length === 0 ) return null;
    let nodes = this.props.options.map( (d, i) => {
      let isActive = (i === this.props.selectionIndex);
      let _className = style.autoListItem;
      if (isActive) _className = `${style.autoListItem} ${style.activeAutoListItem}`;
      return (
        <div className={_className} key={`sbo.${i}`}>
          <span>{d}</span>
        </div>
      );
    });
    return (
      <div className={style.autoList}>
        {nodes}
      </div>
    );
  }
}

OptionsList.propTypes = {
  options: React.PropTypes.array,
  selectionIndex: React.PropTypes.number
};

export default OptionsList;
