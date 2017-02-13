import fetchData from '../lib/fetchData';

export const FETCH_GENE = 'FETCH_GENE';
export const FETCH_GENE_SUCCESS = 'FETCH_GENE_SUCCESS';
export const FETCH_GENE_FAILURE = 'FETCH_GENE_FAILURE';

export function fetchGene(id) {
  return {
    type: FETCH_GENE,
    payload: fetchData('/api/gene/' + id),
  };
}

export function fetchGeneSuccess(gene) {
  return {
    type: FETCH_GENE_SUCCESS,
    payload: gene,
  };
}

export function fetchGEneFailure(error) {
  return {
    type: FETCH_GENE_FAILURE,
    payload: error,
  };
}
