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
    selectSearch(),
    (search) => search.errorMessage
);

const selectIsError = () => createSelector(
    selectSearch(),
    (search) => search.isError
);

const selectResults = () => createSelector(
    selectSearch(),
    (search) => search.results
);

const selectTotal = () => createSelector(
    selectSearch(),
    (search) => search.total
);

export {
    selectSearchDomain,
    selectSearch,
    selectErrorMessage,
    selectIsError,
    selectResults,
    selectTotal,
};
