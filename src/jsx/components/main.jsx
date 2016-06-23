import React from "react";
import injectTapEventPlugin from "react-tap-event-plugin";
import request from "superagent";

import getMuiTheme from "material-ui/styles/getMuiTheme";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

import CircularProgress from "material-ui/CircularProgress";
import Dialog from "material-ui/Dialog";
import Dropzone from 'react-dropzone';
import FlatButton from "material-ui/FlatButton";

import Footer from "./footer";
import FormattedError from "./error";


injectTapEventPlugin();

var config = require("../config/index");


export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        mission: null
      , error: null
      , isWaitingForResponse: false
    };

    this.handleDrop = this.handleDrop.bind(this);
    this.handleErrorClose = this.handleErrorClose.bind(this);
  }

  handleDrop(fileArray) {
    var file = fileArray[0]
      , self = this;

    function _beforeRequest() {
      self.setState({
          mission: null
        , error: null
        , isWaitingForResponse: true
      });
    }

    function _makeRequest() {
      request
        .post(config.parserURL)
        .attach("file", file)
        .end(_onResponse)
    }

    function _onResponse(error, response) {
      var mission = null
        , errorInfo = null;

      if (!response) {
        errorInfo = {
          detail: error.message
        };
      } else if (!response.body) {
        errorInfo = {
          detail: response.statusText
        };
      } else if (!response.ok) {
        errorInfo = response.body;
      } else {
        mission = response.body;
      }

      self.setState({
          mission: mission
        , error: errorInfo
        , isWaitingForResponse: false
      });
    }

    setTimeout(_beforeRequest, 0);
    setTimeout(_makeRequest, 0);
  }

  handleErrorClose() {
    this.setState({
        mission: null
      , error: null
      , isWaitingForResponse: false
    });
  }

  render() {
    const errorActions = [
      <FlatButton
        label="Close"
        primary={true}
        onTouchTap={this.handleErrorClose}
      />,
    ];

    return (
      <MuiThemeProvider muiTheme={getMuiTheme()}>
        <div>
          <article>
            <h1>il2fb-mission-parser demo</h1>
            <h3></h3>
            <Dropzone onDrop={this.handleDrop} className="dropzone" multiple={false}>
              <div>Click here to select mission file or drop it here.</div>
            </Dropzone>
          </article>

          <Footer />

          <Dialog
            title="Waiting for server..."
            modal={true}
            open={this.state.isWaitingForResponse}
            contentClassName="response-wait-dialog-content"
          >
            <CircularProgress />
          </Dialog>

          <Dialog
            title="Error"
            actions={errorActions}
            modal={true}
            open={this.state.error}
            onRequestClose={this.handleErrorClose}
            autoScrollBodyContent={true}
            bodyClassName="error-dialog-content"
          >
            <FormattedError error={this.state.error}/>
          </Dialog>

        </div>
      </MuiThemeProvider>
    );
  }

}
