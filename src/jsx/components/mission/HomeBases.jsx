import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class HomeBaseItem extends React.Component {

  render() {
    var data = this.props.data;

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title={"Home base #" + this.props.index}
        />
        <CardText>
          Homebase
        </CardText>
      </Card>
    );
  }

}


class NoHomeBases extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Home bases" />
        <CardText>
          N/A
        </CardText>
      </Card>
    );
  }

}


export default class HomeBases extends React.Component {

  render() {
    var items = ((this.props.data || {}).objects || {}).home_bases || [];

    if (items.length > 0) {
      var children = items.map(function(data, i) {
        return (<HomeBaseItem key={i} index={i} data={data} />);
      });

      return (<div>{children}</div>);
    } else {
      return (<NoHomeBases />);
    }
  }

}
