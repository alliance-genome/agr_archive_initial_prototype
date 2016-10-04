import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';

import { SearchComponent } from './index';
import Table from './resultsTable';

describe('Search', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<SearchComponent results={[]} total={0} />);
    assert.equal(typeof htmlString, 'string');
  });
});

describe('Table', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<Table entries={[]} />);
    assert.equal(typeof htmlString, 'string');
  });
});

