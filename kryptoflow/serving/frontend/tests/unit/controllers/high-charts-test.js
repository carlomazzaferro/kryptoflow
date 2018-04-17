import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Controller | high-charts', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let controller = this.owner.lookup('controller:high-charts');
    assert.ok(controller);
  });
});
