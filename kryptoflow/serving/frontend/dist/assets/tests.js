'use strict';

define('frontend/tests/app.lint-test', [], function () {
  'use strict';

  QUnit.module('ESLint | app');

  QUnit.test('app.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'app.js should pass ESLint\n\n');
  });

  QUnit.test('components/chart-highstock-interactive.js', function (assert) {
    assert.expect(1);
    assert.ok(false, 'components/chart-highstock-interactive.js should pass ESLint\n\n1:10 - \'copy\' is defined but never used. (no-unused-vars)\n9:9 - Use import { inject } from \'@ember/service\'; instead of using Ember.inject.service (ember/new-module-imports)\n11:3 - Only string, number, symbol, boolean, null, undefined, and function are allowed as default properties (ember/avoid-leaking-state-in-ember-objects)\n36:68 - \'stockData\' is not defined. (no-undef)\n37:7 - Unexpected console statement. (no-console)\n42:69 - \'stockData\' is not defined. (no-undef)');
  });

  QUnit.test('controllers/chart-highstock-interactive.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'controllers/chart-highstock-interactive.js should pass ESLint\n\n');
  });

  QUnit.test('resolver.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'resolver.js should pass ESLint\n\n');
  });

  QUnit.test('router.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'router.js should pass ESLint\n\n');
  });

  QUnit.test('routes/about.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'routes/about.js should pass ESLint\n\n');
  });

  QUnit.test('routes/charts.js', function (assert) {
    assert.expect(1);
    assert.ok(false, 'routes/charts.js should pass ESLint\n\n2:10 - \'copy\' is defined but never used. (no-unused-vars)\n3:20 - \'service\' is defined but never used. (no-unused-vars)');
  });

  QUnit.test('routes/contact.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'routes/contact.js should pass ESLint\n\n');
  });

  QUnit.test('routes/index.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'routes/index.js should pass ESLint\n\n');
  });

  QUnit.test('services/dynamic-chart.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'services/dynamic-chart.js should pass ESLint\n\n');
  });
});
define('frontend/tests/helpers/ember-keyboard/register-test-helpers', ['exports', 'ember-keyboard'], function (exports, _emberKeyboard) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });

  exports.default = function () {
    Ember.Test.registerAsyncHelper('keyDown', function (app, attributes) {
      return keyEvent(app, attributes, 'keydown');
    });

    Ember.Test.registerAsyncHelper('keyUp', function (app, attributes) {
      return keyEvent(app, attributes, 'keyup');
    });

    Ember.Test.registerAsyncHelper('keyPress', function (app, attributes) {
      return keyEvent(app, attributes, 'keypress');
    });
  };

  const keyEvent = function keyEvent(app, attributes, type) {
    const event = attributes.split('+').reduce((event, attribute) => {
      if (['ctrl', 'meta', 'alt', 'shift'].indexOf(attribute) > -1) {
        event[`${attribute}Key`] = true;
      } else {
        event.keyCode = (0, _emberKeyboard.getKeyCode)(attribute);
      }

      return event;
    }, {});

    return app.testHelpers.triggerEvent(document, type, event);
  };
});
define('frontend/tests/test-helper', ['frontend/app', 'frontend/config/environment', '@ember/test-helpers', 'ember-qunit'], function (_app, _environment, _testHelpers, _emberQunit) {
  'use strict';

  (0, _testHelpers.setApplication)(_app.default.create(_environment.default.APP));

  (0, _emberQunit.start)();
});
define('frontend/tests/tests.lint-test', [], function () {
  'use strict';

  QUnit.module('ESLint | tests');

  QUnit.test('test-helper.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'test-helper.js should pass ESLint\n\n');
  });

  QUnit.test('unit/adapters/historic-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/adapters/historic-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/controllers/high-charts-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/controllers/high-charts-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/controllers/historical-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/controllers/historical-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/models/historical-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/models/historical-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/routes/about-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/routes/about-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/routes/charts-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/routes/charts-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/routes/contact-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/routes/contact-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/routes/index-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/routes/index-test.js should pass ESLint\n\n');
  });

  QUnit.test('unit/services/dynamic-chart-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'unit/services/dynamic-chart-test.js should pass ESLint\n\n');
  });

  QUnit.test('units/charts/gdax-test.js', function (assert) {
    assert.expect(1);
    assert.ok(true, 'units/charts/gdax-test.js should pass ESLint\n\n');
  });
});
define('frontend/tests/unit/adapters/historic-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Adapter | historic', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    // Replace this with your real tests.
    (0, _qunit.test)('it exists', function (assert) {
      let adapter = this.owner.lookup('adapter:historic');
      assert.ok(adapter);
    });
  });
});
define('frontend/tests/unit/controllers/high-charts-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Controller | high-charts', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    // Replace this with your real tests.
    (0, _qunit.test)('it exists', function (assert) {
      let controller = this.owner.lookup('controller:high-charts');
      assert.ok(controller);
    });
  });
});
define('frontend/tests/unit/controllers/historical-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Controller | historical', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    // Replace this with your real tests.
    (0, _qunit.test)('it exists', function (assert) {
      let controller = this.owner.lookup('controller:historical');
      assert.ok(controller);
    });
  });
});
define('frontend/tests/unit/models/historical-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Model | historical', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    // Replace this with your real tests.
    (0, _qunit.test)('it exists', function (assert) {
      let store = this.owner.lookup('service:store');
      let model = Ember.run(() => store.createRecord('historical', {}));
      assert.ok(model);
    });
  });
});
define('frontend/tests/unit/routes/about-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Route | about', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    (0, _qunit.test)('it exists', function (assert) {
      let route = this.owner.lookup('route:about');
      assert.ok(route);
    });
  });
});
define('frontend/tests/unit/routes/charts-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Route | charts', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    (0, _qunit.test)('it exists', function (assert) {
      let route = this.owner.lookup('route:charts');
      assert.ok(route);
    });
  });
});
define('frontend/tests/unit/routes/contact-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Route | contact', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    (0, _qunit.test)('it exists', function (assert) {
      let route = this.owner.lookup('route:contact');
      assert.ok(route);
    });
  });
});
define('frontend/tests/unit/routes/index-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Route | index', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    (0, _qunit.test)('it exists', function (assert) {
      let route = this.owner.lookup('route:index');
      assert.ok(route);
    });
  });
});
define('frontend/tests/unit/services/dynamic-chart-test', ['qunit', 'ember-qunit'], function (_qunit, _emberQunit) {
  'use strict';

  (0, _qunit.module)('Unit | Service | dynamic-chart', function (hooks) {
    (0, _emberQunit.setupTest)(hooks);

    // Replace this with your real tests.
    (0, _qunit.test)('it exists', function (assert) {
      let service = this.owner.lookup('service:dynamic-chart');
      assert.ok(service);
    });
  });
});
define('frontend/tests/units/charts/gdax-test', ['ember-qunit'], function (_emberQunit) {
  'use strict';

  (0, _emberQunit.moduleForComponent)('gdax', 'gdax', {
    needs: ['component:high-charts']
  });

  (0, _emberQunit.test)('it renders', function (assert) {
    assert.expect(2);

    // creates the component instance
    let component = this.subject();
    assert.equal(component._state, 'preRender');

    // appends the component to the page
    this.render(assert);
    assert.equal(component._state, 'inDOM');
  });
});
define('frontend/config/environment', [], function() {
  var prefix = 'frontend';
try {
  var metaName = prefix + '/config/environment';
  var rawConfig = document.querySelector('meta[name="' + metaName + '"]').getAttribute('content');
  var config = JSON.parse(unescape(rawConfig));

  var exports = { 'default': config };

  Object.defineProperty(exports, '__esModule', { value: true });

  return exports;
}
catch(err) {
  throw new Error('Could not read config from meta tag with name "' + metaName + '".');
}

});

require('frontend/tests/test-helper');
EmberENV.TESTS_FILE_LOADED = true;
//# sourceMappingURL=tests.map
