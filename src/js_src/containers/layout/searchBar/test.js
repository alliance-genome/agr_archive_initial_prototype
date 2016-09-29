import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';

import { SearchBarComponent } from './index';

describe('Search Bar', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<SearchBarComponent />);
    assert.equal(typeof htmlString, 'string');
  });
});
