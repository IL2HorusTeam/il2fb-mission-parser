var webpack = require('webpack');
var path = require('path');

var APP_DIR = path.resolve(__dirname, 'src/jsx/');
var BUILD_DIR = path.resolve(__dirname, 'build/');

var config = {
  devtool: 'eval'
  , entry: APP_DIR + '/app.jsx'
  , output: {
    path: BUILD_DIR
    , filename: 'bundle.js'
  }
  , resolve: {
    extensions: ['', '.js', '.jsx']
  }
  , module: {
    loaders: [
      {
        test: /\.jsx?$/
        , loader: 'babel'
        , include : APP_DIR
        , exclude: /node_modules/
        , query: {
          cacheDirectory: true
          , presets: ['react', 'es2015']
        }
      }
    ]
  }
  , plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('development')
      }
    })
  ]
};

module.exports = config;
