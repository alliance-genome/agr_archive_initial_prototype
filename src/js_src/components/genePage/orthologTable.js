import React, { Component } from 'react';

const columnNames = ['Species', 'Gene symbol', 'NCBI gene', 'Score',
  'Best score', 'Best reverse score', 'Source', 'Align'];

const ALL_SOURCES = {
  compara: {
    name: 'Compara'
  },
  homologene: {
    name: 'Homologene'
  },
  inparanoid: {
    name: 'Inparanoid'
  },
  isobase: {
    name: 'Isobase'
  },
  oma: {
    name: 'OMA',
  },
  orthodb: {
    name: 'OrthoDB'
  },
  orthomcl: {
    name: 'orthoMCL'
  },
  panther: {
    name: 'Panther'
  },
  phylome: {
    name: 'Phylome'
  },
  roundup: {
    name: 'RoundUp'
  },
  treefam: {
    name: 'TreeFam'
  },
  zfin: {
    name: 'ZFIN'
  }
};

const sourceCellStyle = {
  width: 20,
  display: 'inline-block'
};

const SourceColumnHeader = () => (<th>
  <div>Source</div>
  <div style={{minWidth: 20 * Object.keys(ALL_SOURCES).length}}>{
    Object.keys(ALL_SOURCES).sort().map((sourceKey) => (
      <span key={sourceKey} style={sourceCellStyle}>
      {
        sourceKey[0]
      }
      </span>
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
