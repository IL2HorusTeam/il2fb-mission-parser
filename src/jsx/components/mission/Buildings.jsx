import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class NoBuildings extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no buildings.
        </CardText>
      </Card>
    );
  }

}


export default class Buildings extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).buildings || [];

    if (list.length === 0) {
      return (<NoBuildings />);
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
