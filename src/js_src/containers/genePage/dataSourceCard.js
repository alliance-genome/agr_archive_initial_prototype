import React, {Component} from 'react';

import DataSourceLink from '../../components/dataSourceLink';

import style from './style.css';

class DataSourceCard extends Component {
  render() {
    let d = this.props.sourceData;
    return (
      <div className='card'>
        <div className={`${style.speciesIcon} ${style[d.dataProvider]}`} />
        <div className='card-block'>
          <dl className='row'>
            <dt className='col-sm-5'>Species</dt>
            <dd className='col-sm-7'><i>{d.species}</i></dd>
            <dt className='col-sm-5'>Primary Source</dt>
            <dd className='col-sm-7'>
              <DataSourceLink dataProvider={d.dataProvider} id={d.primaryId} />
            </dd>
          </dl>
        </div>
      </div>
    );
  }
}

DataSourceCard.propTypes = {
  sourceData: React.PropTypes.object
};

export default DataSourceCard;
