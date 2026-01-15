import * as assert from 'assert';

import { Config } from '../config/config';

describe('Config finderMode', () => {
  it('should get and set finder mode via property', () => {
    const cfg = new Config();
    // default mode from FinderConfig defaults to 'char'
    assert.equal(cfg.finderMode, 'char');

    cfg.finderMode = 'regex';
    assert.equal(cfg.finderMode, 'regex');
  });
});
