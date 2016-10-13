import React, { Component } from 'react';

import style from './style.css';
import { makeFieldDisplayName } from '../../lib/searchHelpers';

class DetailList extends Component {
  render() {
    let d = this.props.data;
    let nodes = this.props.fields.map( (field) => {
      return (
        <div className={style.detailLineContainer} key={`srField.${field}`}>
          <span className={style.detailLabel}><strong>{makeFieldDisplayName(field)}:</strong> </span>
          <span dangerouslySetInnerHTML={{ __html: d[field] }} />
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
