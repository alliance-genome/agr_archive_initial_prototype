import React, { Component } from 'react';

import style from './style.css';
import { makeFieldDisplayName } from '../../lib/searchHelpers';

class DetailList extends Component {
  render() {
    let d = this.props.data;
    let nodes = this.props.fields.map( (field) => {
      let valueNode;
      if (field === 'species') {
        valueNode = <span><i dangerouslySetInnerHTML={{ __html: d[field] }} /></span>;
      } else {
        valueNode = <span dangerouslySetInnerHTML={{ __html: d[field] }} />;
      }
      return (
        <div className={style.detailLineContainer} key={`srField.${field}`}>
          <span className={style.detailLabel}><strong>{makeFieldDisplayName(field)}:</strong> </span>
          {valueNode}
        </div>
      );
    });
    return (
      <div className={style.detailContainer}>
        {nodes}
      </div>
    );
  }
}

DetailList.propTypes = {
  data: React.PropTypes.object,
  fields: React.PropTypes.array
};

export default DetailList;
