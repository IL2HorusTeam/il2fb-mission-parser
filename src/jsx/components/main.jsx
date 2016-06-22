import React from "react";
import injectTapEventPlugin from "react-tap-event-plugin";
import request from "superagent";

import getMuiTheme from "material-ui/styles/getMuiTheme";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

import CircularProgress from 'material-ui/CircularProgress';
import Dialog from 'material-ui/Dialog';
import Dropzone from "react-dropzone";

import Footer from "./footer";


injectTapEventPlugin();

var config = require("../config/index");


export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      mission: null
      , is_waiting_response: false
    };

    this.onDrop = this.onDrop.bind(this);
  }

  onDrop(fileArray) {
    var file = fileArray[0]
        , self = this;

    function _showRequestModal() {
      self.setState({
        response: null
        , is_waiting_response: true
      });
    }

    function _makeRequest() {
      var mission = null;

      request
        .post(config.parserURL)
        .attach("file", file)
        .end(function(error, response) {

          if (error || !response.ok) {
            console.log("Oh no! error");
          } else {
            mission = response.body;
          }

          self.setState({
            response: mission
            , is_waiting_response: false
          });
        })
    }

    setTimeout(_showRequestModal, 0);
    setTimeout(_makeRequest, 0);
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={getMuiTheme()}>
        <div>
          <article>
            <h1>il2fb-mission-parser demo</h1>
            <h3></h3>

            <Dropzone onDrop={this.onDrop} className="dropzone" multiple={false}>
              <div>Click here to select mission file or drop it here.</div>
            </Dropzone>

          </article>

          <Footer />

          <Dialog
            title="Waiting for server..."
            modal={true}
            open={this.state.is_waiting_response}
            contentClassName="response-wait"
          >
            <CircularProgress />
          </Dialog>
        </div>
      </MuiThemeProvider>
    );
  }

}
