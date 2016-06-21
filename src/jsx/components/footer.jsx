import React from "react";

import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FontIcon from 'material-ui/FontIcon';
import RaisedButton from 'material-ui/RaisedButton';


class PageInfoButton extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      open: false
    };

    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen() {
    this.setState({open: true});
  };

  handleClose() {
    this.setState({open: false});
  };

  render() {
    const actions = [
      <FlatButton
        label="Close"
        primary={true}
        onTouchTap={this.handleClose}
      />,
    ];

    return (
      <div>
        <RaisedButton
          label="About"
          onTouchTap={this.handleOpen}
          icon={<FontIcon className="material-icons">info_outline</FontIcon>}
        />
        <Dialog
          title="Page info"
          actions={actions}
          modal={true}
          open={this.state.open}
          onRequestClose={this.handleClose}
          className="dialog"
        >
          <p>
            This is a demo page of "il2fb-mission-parser" — a Python library
            for parsing mission files of aviasimulator called
            "IL-2&nbsp;Sturmovik:&nbsp;Forgotten&nbsp;Battles".
          </p>
          <p>
            "il2fb-mission-parser" library allows you to extract any data
            contained within mission files.
          </p>
          <p>
            This page is used for testing library out of the browser.
            Here you can upload your mission file and see extracted and
            visualized data.
          </p>
          <p>
            Please, find more information following links at the bottom of this
            page.
          </p>
        </Dialog>
      </div>
    );
  }

}

export default class Footer extends React.Component {

  render() {
    return (
      <footer>
        <div className="footer-buttons">
          <PageInfoButton />
          <RaisedButton
            label="Docs"
            icon={<FontIcon className="material-icons">school</FontIcon>}
            linkButton={true}
            href="http://il-2-missions-parser.rtfd.org/"
          />
          <RaisedButton
            label="Sources"
            icon={<FontIcon className="material-icons">code</FontIcon>}
            linkButton={true}
            href="https://github.com/IL2HorusTeam/il2fb-mission-parser/"
          />
          <RaisedButton
            label="Issues"
            icon={<FontIcon className="material-icons">bug_report</FontIcon>}
            linkButton={true}
            href="https://github.com/IL2HorusTeam/il2fb-mission-parser/issues/"
          />
        </div>
      </footer>
    );
  }

}
