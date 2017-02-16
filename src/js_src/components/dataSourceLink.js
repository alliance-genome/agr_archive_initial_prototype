import React, {Component} from 'react';

const URL_GENERATORS = {
  FB: id => `http://flybase.org/reports/${id}.html`,
  MGI: id => `http://www.informatics.jax.org/marker/${id}`,
  RGD: id => `http://rgd.mcw.edu/rgdweb/report/gene/main.html?id=${id}`,
  SGD: id => `http://www.yeastgenome.org/locus/${id}/overview`,
  ZFIN: id => `https://zfin.org/${id}`,
  WB: id => `http://www.wormbase.org/species/c_elegans/gene/${id}`,
  NCBIGene: id => `https://www.ncbi.nlm.nih.gov/gene/?term=${id}`,
  UniProtKB: id => `http://www.uniprot.org/uniprot/${id}`,
  Ensembl: id => `http://www.ensembl.org/id/${id}`,
  RNAcentral: id => `http://rnacentral.org/rna/${id}`,
  HGNC: id => `http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=${id}`
};

class DataSourceLink extends Component {
  render() {
    let linker = URL_GENERATORS[this.props.dataProvider];
    if (!linker) {
      return <span>{this.props.dataProvider}:{this.props.id}</span>;
    }
    return (
      <span>
        {this.props.dataProvider}:<a href={linker(this.props.id)}>{this.props.id}</a>
      </span>
    );
  }
}

DataSourceLink.propTypes = {
  dataProvider: React.PropTypes.string,
  id: React.PropTypes.string,
};

export default DataSourceLink;
