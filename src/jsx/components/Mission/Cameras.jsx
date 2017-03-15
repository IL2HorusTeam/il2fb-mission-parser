import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class NoCameras extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no cameras.
        </CardText>
      </Card>
    );
  }

}


export default class Cameras extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).cameras || [];

    if (list.length === 0) {
      return (<NoCameras />);
    }

    var entries = list.map(function(data, i) {
      return (
        <TableRow className="row" hoverable={true} key={i}>
          <TableRowColumn>
            {i}
          </TableRowColumn>

          <TableRowColumn className={data.belligerent.name}>
            {data.belligerent.verbose_name}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.x.toFixed(2)}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.y.toFixed(2)}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.z.toFixed(2)}
          </TableRowColumn>
        </TableRow>
      );
    });

    return (
      <Card className="mission-details-card">
        <CardText>
          <Table className="table">
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn>#</TableHeaderColumn>
                <TableHeaderColumn>Belligerent</TableHeaderColumn>
                <TableHeaderColumn>X, m</TableHeaderColumn>
                <TableHeaderColumn>Y, m</TableHeaderColumn>
                <TableHeaderColumn>Z, m</TableHeaderColumn>
              </TableRow>
            </TableHeader>
            <TableBody displayRowCheckbox={false} showRowHover={true}>
              {entries}
            </TableBody>
          </Table>
        </CardText>
      </Card>
    );
  }

}
