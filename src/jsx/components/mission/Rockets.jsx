import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class NoRockets extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no rockets.
        </CardText>
      </Card>
    );
  }

}


export default class Rockets extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).rockets || [];

    if (list.length === 0) {
      return (<NoRockets />);
    }

    var entries = list.map(function(data, i) {
      return (
        <TableRow className="row" hoverable={true} key={i}>
          <TableRowColumn>
            {data.id}
          </TableRowColumn>

          <TableRowColumn>
            {data.code}
          </TableRowColumn>

          <TableRowColumn className={data.belligerent.name}>
            {data.belligerent.verbose_name}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.x}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.y}
          </TableRowColumn>

          <TableRowColumn>
            {data.rotation_angle}
          </TableRowColumn>

          <TableRowColumn>
            {data.delay}
          </TableRowColumn>

          <TableRowColumn>
            {data.count}
          </TableRowColumn>

          <TableRowColumn>
            {data.period}
          </TableRowColumn>

          <TableRowColumn>
            {
              data.destination
              ? data.destination.x
              : "—"
            }
          </TableRowColumn>

          <TableRowColumn>
            {
              data.destination
              ? data.destination.y
              : "—"
            }
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
                <TableHeaderColumn>ID</TableHeaderColumn>
                <TableHeaderColumn>Code</TableHeaderColumn>
                <TableHeaderColumn>Belligerent</TableHeaderColumn>
                <TableHeaderColumn>X, m</TableHeaderColumn>
                <TableHeaderColumn>Y, m</TableHeaderColumn>
                <TableHeaderColumn>Angle, °</TableHeaderColumn>
                <TableHeaderColumn>Delay, min</TableHeaderColumn>
                <TableHeaderColumn>Count</TableHeaderColumn>
                <TableHeaderColumn>Period, min</TableHeaderColumn>
                <TableHeaderColumn>Destination X, m</TableHeaderColumn>
                <TableHeaderColumn>Destination Y, m</TableHeaderColumn>
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
