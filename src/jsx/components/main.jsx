import React from 'react';
import Dropzone from 'react-dropzone';
import request from 'superagent';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

var config = require('../config/index.jsx');

export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      data: null
    };
  }

  onDrop(fileArray) {
    var file = fileArray[0];
    request
      .post(config.parserURL)
      .attach('file', file)
      .end(function(err, res) {
        if (err || !res.ok) {
          console.log('Oh no! error');
        } else {
          console.log(res.body);
        }
      })
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={getMuiTheme()}>
        <div>
          <h1>il2fb-mission-parser demo</h1>
          <h3></h3>
          <Dropzone onDrop={this.onDrop} className='dropzone' multiple={false}>
            <div>Start by selecting your mission file. Click or drop here.</div>
          </Dropzone>
        </div>
      </MuiThemeProvider>
    );
  }
}
