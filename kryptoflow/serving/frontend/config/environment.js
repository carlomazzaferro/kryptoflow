'use strict';

module.exports = function(environment) {
  let ENV = {
    'ember-websockets': {
      socketIO: true
    },
    modulePrefix: 'frontend',
    environment,
    rootURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
    // contentSecurityPolicy: {
    //   'default-src': "'none'",
    //   'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
    //   'font-src': "'self'",
    //   'connect-src': "'self' ws://0.0.0.0:5000 0.0.0.0:5000",
    //   'img-src': "'self'",
    //   'report-uri':"'0.0.0.0'",
    //   'style-src': "'self' 'unsafe-inline'",
    //   'frame-src': "'none'"
    // }
  };

  ENV['x-toggle'] = {
    includedThemes: ['light', 'default', 'flip'],
    excludedThemes: ['flip'],
    excludeBaseStyles: false, // defaults to false
    defaultShowLabels: true,  // defaults to false
    defaultTheme: 'light',    // defaults to 'default'
    defaultSize: 'small',     // defaults to 'medium'
    defaultOffLabel: 'False', // defaults to 'Off'
    defaultOnLabel: 'True'    // defaults to 'On'
  };


  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
    ENV.APP.autoboot = false;
  }

  if (environment === 'production') {
    // here you can enable a production-specific feature
  }

  return ENV;
};


