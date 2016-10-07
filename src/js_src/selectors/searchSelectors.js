import { createSelector } from 'reselect';

// See https://github.com/reactjs/reselect
// for details on using selectors.

/**
 * Direct selector to the search state.
 */
const selectSearchDomain = () => state => state.get('search');

const selectSearch = () => createSelector(
    selectSearchDomain(),
    (searchDomain) => searchDomain.toJS()
);

const selectErrorMessage = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('errorMessage')
);

const selectIsError = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('isError')
);

const selectResults = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('results').toJS()
);

const selectTotal = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('total')
);

const selectActiveCategory = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('activeCategory')
);
const selectAggregations = () => createSelector(
    selectSearchDomain(),
    (search) => search.get('aggregations').toJS()
);

export {
    selectSearchDomain,
    selectSearch,
    selectErrorMessage,
    selectIsError,
    selectResults,
    selectTotal,
    selectActiveCategory,
    selectAggregations,
};
