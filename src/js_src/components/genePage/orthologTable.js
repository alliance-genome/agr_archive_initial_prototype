import React, { Component } from 'react';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';


const columnNames = ['Species', 'Gene symbol', 'Score',
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

const sourceCellWidth = 25;

const sourceCellStyle = {
  width: sourceCellWidth,
  display: 'inline-block',
  textAlign: 'center',
  lineHeight: '20px',
};

const SourceLogo = ({sourceKey}) => {
  const sourceName = ALL_SOURCES[sourceKey] ?
    ALL_SOURCES[sourceKey].name : sourceKey;

  const tooltip = (
    <Tooltip
      className="in"
      id="tooltip-bottom"
      placement="bottom"
    >
    {
      sourceName
    }
    </Tooltip>
  );

  const hasIcon = ALL_SOURCES[sourceKey] && ALL_SOURCES[sourceKey].icon;
  return (
    <OverlayTrigger
      delayHide={150}
      delayShow={300}
      overlay={tooltip}
      placement="top"
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
  <div style={{minWidth: sourceCellWidth * Object.keys(ALL_SOURCES).length}}>{
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
      Object.keys(ALL_SOURCES).map((source) => {
        const tipText = sourceSet.has(source) ?
          `Found in ${ALL_SOURCES[source].name}` :
          `Not found in ${ALL_SOURCES[source].name}`;

        const tooltip = (
          <Tooltip
            className="in"
            id="tooltip-bottom"
            placement="bottom"
          >
          {
            tipText
          }
          </Tooltip>
        );

        return (
          <OverlayTrigger
            delayHide={150}
            delayShow={300}
            key={source}
            overlay={tooltip}
            placement="top"
          >
            <span style={sourceCellStyle}>
            {
              sourceSet.has(source) ? '\u25A0' : '\u00a0'
            }
            </span>
          </OverlayTrigger>
        );
      })
    }
    </td>
  );
};

SourceColumnData.propTypes = {
  sources: React.PropTypes.arrayOf(React.PropTypes.string),
};

const BooleanCell = ({value, labelTrue, labelFalse}) => {
  const backgroundColor = value ? '#dff0d8' : 'transparent';
  return (
    <td
      style={{
        backgroundColor: backgroundColor,
      }}
    >
    {
      value ? (labelTrue || 'Yes') : (labelFalse || 'No')
    }
    </td>
  );
};

BooleanCell.propTypes = {
  labelFalse: React.PropTypes.string,
  labelTrue: React.PropTypes.string,
  value: React.PropTypes.bool,
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
                return (<SourceColumnHeader key={columnName} />);
              } else {
                return (<th key={columnName}>{columnName}</th>);
              }
            })
          }
          </tr>
        </thead>
        <tbody>
        {
          this.props.data.map((orthData) => {
            return (
              <tr key={`${orthData.species}-${orthData.geneSymbol}`}>
                <td>{orthData.species}</td>
                <td>
                  <a href={orthData.geneURL}>{orthData.geneSymbol}</a>
                  <span
                    style={{
                      display: 'inline-block',
                      margin: '0 0.5em'
                    }}
                  >|</span>
                  <a href={`https://www.ncbi.nlm.nih.gov/gene/${orthData.ncbiID}`}>[NCBI]</a>
                </td>
                <td>{`${orthData.scoreNumerator} of ${orthData.scoreDemominator}`}</td>
                <BooleanCell value={orthData.isBestScore} />
                <BooleanCell value={orthData.isBestScoreReverse} />
                <SourceColumnData sources={orthData.sources} />
                <td><a href={orthData.alignURL}>View</a></td>
              </tr>
            );
          })
        }
        </tbody>
      </table>
    );
  }
}

OrthologTable.propTypes = {
  data: React.PropTypes.arrayOf(
    React.PropTypes.shape({
      species: React.PropTypes.string,
      geneSymbol: React.PropTypes.string,
      geneURL: React.PropTypes.string,
      ncbiID: React.PropTypes.string,
      scoreNumerator: React.PropTypes.number,
      scoreDemominator: React.PropTypes.number,
      isBestScore: React.PropTypes.bool,
      isBestScoreReverse: React.PropTypes.bool,
      alignURL: React.PropTypes.string,
    })
  )
};

export default OrthologTable;
