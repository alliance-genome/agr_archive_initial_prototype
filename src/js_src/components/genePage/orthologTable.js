import React, { Component } from 'react';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';


const columnNames = ['Species', 'Gene symbol', 'NCBI gene', 'Score',
  'Best score', 'Best reverse score', 'Source', 'Align'];

const ALL_SOURCES = {
  compara: {
    name: 'Compara',
    icon: 'http://static.ensembl.org/i/ensembl-favicon.png'
  },
  homologene: {
    name: 'Homologene',
    icon: 'https://www.ncbi.nlm.nih.gov/favicon.ico'
  },
  inparanoid: {
    name: 'Inparanoid',
    icon: 'http://inparanoid.sbc.su.se/favicon.ico'
  },
  isobase: {
    name: 'Isobase',
  },
  oma: {
    name: 'OMA',
    icon: 'https://omictools.com/img/apple-touch-icon.png'
  },
  orthodb: {
    name: 'OrthoDB',
  },
  orthomcl: {
    name: 'orthoMCL',
    icon: 'http://orthomcl.org/orthomcl/images/OrthoMCL/favicon.ico'
  },
  panther: {
    name: 'Panther',
    icon: 'http://www.pantherdb.org/favicon.ico'
  },
  phylome: {
    name: 'Phylome',
    icon: 'http://phylomedb.org/sites/default/files/images/phylomedb.ico'
  },
  roundup: {
    name: 'RoundUp'
  },
  treefam: {
    name: 'TreeFam',
    icon: 'http://www.treefam.org/static/images/favicon.png'
  },
  zfin: {
    name: 'ZFIN',
    icon: 'https://zfin.org/images/zfinlogo.png'
//    icon: 'https://zfin.org/favicon.ico'
  }
};

const sourceCellStyle = {
  width: 20,
  display: 'inline-block',
  textAlign: 'center',
  lineHeight: '20px',
};

const SourceLogo = ({sourceKey}) => {
  const sourceName = ALL_SOURCES[sourceKey] ?
    ALL_SOURCES[sourceKey].name : sourceKey;

    const tooltip = (<Tooltip
      className="in"
      id="tooltip-bottom"
      placement="bottom"
    >
    {
      sourceName
    }
    </Tooltip>);

  const hasIcon = ALL_SOURCES[sourceKey] && ALL_SOURCES[sourceKey].icon;
  return (
    <OverlayTrigger
      overlay={tooltip} placement="top"
      delayShow={300} delayHide={150}
    >
      <span style={sourceCellStyle}>
      {
        hasIcon ?
          <img
            alt={sourceName}
            height={16}
            src={ALL_SOURCES[sourceKey].icon}
            width={16}
          /> :
          sourceName.substring(0, 1)
      }
      </span>
    </OverlayTrigger>
  );
};

SourceLogo.propTypes = {
  sourceKey: React.PropTypes.string
};

const SourceColumnHeader = () => (<th>
  <div>Source</div>
  <div style={{minWidth: 20 * Object.keys(ALL_SOURCES).length}}>{
    Object.keys(ALL_SOURCES).sort().map((sourceKey) => (
      <SourceLogo key={sourceKey} sourceKey={sourceKey} />
    ))
  }</div>
</th>);

const SourceColumnData = ({sources}) => {
  const sourceSet = new Set(sources || []);
  return (
    <td>
    {
      Object.keys(ALL_SOURCES).map((source) => (
        <span key={source} style={sourceCellStyle}>
        {
          sourceSet.has(source) ? '\u25A0' : ''
        }
        </span>
      ))
    }
    </td>
  );
};

SourceColumnData.propTypes = {
  sources: React.PropTypes.arrayOf(React.PropTypes.string),
};

class OrthologTable extends Component {

  render() {
    return(
      <table className='table'>
        <thead>
          <tr>
          {
            columnNames.map((columnName) => {
              if (columnName === 'Source') {
                return (<SourceColumnHeader />);
              } else {
                return (<th>{columnName}</th>);
              }
            })
          }
          </tr>
        </thead>
        <tbody>
        {
          [1,2,3,4,5,6,7,8].map((orthData) => {
            return (<tr key={orthData}>
              <td>NA</td>
              <td>NA</td>
              <td>NA</td>
              <td>NA</td>
              <td>NA</td>
              <td>NA</td>
              <SourceColumnData sources={['compara', 'panther', 'phylome']} />
              <td>NA</td>
            </tr>);
          })
        }
        </tbody>
      </table>
    );
  }
}

export default OrthologTable;
