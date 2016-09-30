import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';

import Table from './index';

describe('Table', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<Table entries={[]} />);
    assert.equal(typeof htmlString, 'string');
  });
});
