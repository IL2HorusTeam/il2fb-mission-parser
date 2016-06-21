import React from "react";
import injectTapEventPlugin from "react-tap-event-plugin";
import Dropzone from "react-dropzone";
import request from "superagent";

import getMuiTheme from "material-ui/styles/getMuiTheme";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

import Footer from "./footer";


injectTapEventPlugin();

var config = require("../config/index");


export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      response: null
    };

    this.onDrop = this.onDrop.bind(this);
  }

  onDrop(fileArray) {
    var file = fileArray[0],
        self = this;

    request
      .post(config.parserURL)
      .attach("file", file)
      .end(function(error, response) {

        if (error || !response.ok) {
          console.log("Oh no! error");

          response = null;
        } else {
          response = response.body;
        }

        self.setState({response: response});
      })
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

        </div>
      </MuiThemeProvider>
    );
  }

}
