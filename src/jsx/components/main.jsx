import React from "react";
import injectTapEventPlugin from "react-tap-event-plugin";
import update from "react-addons-update";

import request from "superagent";

import getMuiTheme from "material-ui/styles/getMuiTheme";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

import CircularProgress from "material-ui/CircularProgress";
import Dialog from "material-ui/Dialog";
import Dropzone from 'react-dropzone';
import FlatButton from "material-ui/FlatButton";

import Footer from "./footer";
import ErrorDialog from "./error";


injectTapEventPlugin();

const config = require("../config/index");


class ResponseWaitDialog extends React.Component {

  render() {
    return (
      <Dialog
        title="Waiting for server..."
        modal={true}
        open={this.props.open}
        contentClassName="response-wait-dialog-content"
      >
        <CircularProgress />
      </Dialog>
    );
  }

}


class Body extends React.Component {

  render() {
    return (
      <article>
        <h1>il2fb-mission-parser demo</h1>
        <h3></h3>

        <Dropzone
          onDrop={this.props.onFileDrop}
          className="dropzone"
          multiple={false}
        >
          <div>
            Click here to select mission file or drop it here.
          </div>
        </Dropzone>
      </article>
    );
  }

}


export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        mission: null
      , error: null
      , isWaitingForResponse: false
    };

    this.handleFileDrop = this.handleFileDrop.bind(this);
    this.handleCloseErrorDialog = this.handleCloseErrorDialog.bind(this);
  }

  handleFileDrop(fileArray) {
    var file = fileArray[0]
      , self = this;

    function _beforeRequest() {
      self.setState(update(self.state, {$merge: {
          error: null
        , isWaitingForResponse: true
      }}));
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

      self.setState(update(self.state, {$merge: {
          mission: mission
        , error: errorInfo
        , isWaitingForResponse: false
      }}));
    }

    setTimeout(_beforeRequest, 0);
    setTimeout(_makeRequest, 0);
  }

  handleCloseErrorDialog() {
    this.setState(update(this.state, {$merge: {
      error: null
    }}));
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={getMuiTheme()}>
        <div>
          <Body
            onFileDrop={this.handleFileDrop}
          />
          <Footer />
          <ResponseWaitDialog
            open={this.state.isWaitingForResponse}
          />
          <ErrorDialog
            onClose={this.handleCloseErrorDialog}
            error={this.state.error}
          />
        </div>
      </MuiThemeProvider>
    );
  }

}
