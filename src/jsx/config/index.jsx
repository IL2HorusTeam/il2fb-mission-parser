var env = process.env.APP_ENV || 'development';

var config = {
  development: require('./development.config.jsx'),
  production: require('./production.config.jsx'),
};

module.exports = config[env];
