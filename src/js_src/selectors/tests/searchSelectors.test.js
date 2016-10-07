import assert from 'assert';
import { fromJS } from 'immutable';

import {
    selectSearchDomain,
    selectSearch,
    selectErrorMessage,
    selectIsError,
    selectResults,
    selectTotal,
    selectActiveCategory,
    selectAggregations,
} from '../searchSelectors';

/*const stateJS = {
    search: {
        errorMessage: 'This is an error',
    }
};
const state = fromJS(stateJS);*/

describe('SearchSelectors', () => {
    const searchDomainSelector = selectSearchDomain();
    it('selectSearchDomain', () => {
        const searchState = fromJS({});
        const mockedState = fromJS({
            search: searchState,
        });
        assert.equal(searchDomainSelector(mockedState),searchState);
    });

    const searchSelector = selectSearch();
    it('selectSearch', () => {
        const searchState = {};
        const mockedState = fromJS({
            search: searchState,
        });
        assert.deepEqual(searchSelector(mockedState),searchState);
    });

    const resultsSelector = selectResults();
    it('selectResults', () => {
        const searchState = { results: [1,2,3,4] };
        const mockedState = fromJS({
            search: searchState,
        });
        assert.deepEqual(resultsSelector(mockedState),searchState.results);
    });

    const errorMessageSelector = selectErrorMessage();
    it('selectErrorMessage', () => {
        const searchState = { errorMessage: 'This is an error' };
        const mockedState = fromJS({
            search: searchState,
        });
        assert.deepEqual(errorMessageSelector(mockedState),searchState.errorMessage);
    });

    const isErrorSelector = selectIsError();
    it('selectIsError', () => {
        const searchState = { isError: true };
        const mockedState = fromJS({
            search: searchState,
        });
        assert.equal(isErrorSelector(mockedState),searchState.isError);
    });

    const totalSelector = selectTotal();
    it('selectTotal', () => {
        const searchState = { total: 10 };
        const mockedState = fromJS({
            search: searchState,
        });
        assert.equal(totalSelector(mockedState),searchState.total);
    });

    const activeCategorySelector = selectActiveCategory();
    it('selectActiveCategory', () => {
        const searchState = { activeCategory: 'my category' };
        const mockedState = fromJS({
            search: searchState,
        });
        assert.equal(activeCategorySelector(mockedState),searchState.activeCategory);
    });

    const aggregationsSelector = selectAggregations();
    it('selectAggregations', () => {
        const searchState = { aggregations: [{name:'myagg1', displayName:'My agg1'},{name:'myagg2', displayName:'My agg2'}]};
        const mockedState = fromJS({
            search: searchState,
        });
        assert.deepEqual(aggregationsSelector(mockedState),searchState.aggregations);
    });
});

