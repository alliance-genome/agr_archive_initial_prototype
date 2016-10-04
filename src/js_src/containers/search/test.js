import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { createMemoryHistory } from 'react-router';
import { Provider } from 'react-redux'

import configureStore from '../../lib/configureStore';
import { SearchComponent } from './index';
import { FilterSelectorComponent } from './filterSelector';
import ResultsTable from './resultsTable';

let historyObj = createMemoryHistory('/search');
let store = configureStore(historyObj);

describe('Search', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<Provider store={store}><SearchComponent results={[]} total={0} /></Provider>);
    assert.equal(typeof htmlString, 'string');
  });
});

describe('ResultsTable', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<ResultsTable entries={[]} />);
    assert.equal(typeof htmlString, 'string');
  });
});

describe('FilterSelector', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<FilterSelectorComponent aggregations={[]} />);
    assert.equal(typeof htmlString, 'string');
  });
});

