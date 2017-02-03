import assert from 'assert';
import React from 'react';
import { renderToString } from 'react-dom/server';

import GenePage from './index';

describe('GenePage', () => {
  it('should be able to render to an HTML string', () => {
    let htmlString = renderToString(<GenePage params={{geneId: 5}} />);
    assert.equal(typeof htmlString, 'string');
  });
});
