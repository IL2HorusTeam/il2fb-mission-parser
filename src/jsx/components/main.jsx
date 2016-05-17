import React from 'react';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import RaisedButton from 'material-ui/RaisedButton';
import {deepOrange500} from 'material-ui/styles/colors';


const styles = {
  container: {
    textAlign: 'center',
    paddingTop: 200,
  },
};


const muiTheme = getMuiTheme({
  palette: {
    accent1Color: deepOrange500,
  },
});


export default class Main extends React.Component {
  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <div style={styles.container}>
          <h1>material-ui</h1>
          <h2>example project</h2>
          <RaisedButton
            label="Hello button"
            primary={true}
          />
        </div>
      </MuiThemeProvider>
    );
  }
}
