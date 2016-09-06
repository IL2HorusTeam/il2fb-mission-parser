import React from "react";

import Checkbox from 'material-ui/Checkbox';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import FontIcon from 'material-ui/FontIcon';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class FlightAircrafts extends React.Component {

  render() {
    var entries = this.props.items.map(function(data, i) {
      return (
        <TableRow className="row" hoverable={true} key={i}>
          <TableRowColumn>
            {data.index}
          </TableRowColumn>

          <TableRowColumn>
            {data.skill.verbose_name}
          </TableRowColumn>

          <TableRowColumn>
            <FontIcon
              className="material-icons"
              color={data.has_markings ? "green" : "red"}
            >
              {data.has_markings ? "check" : "close"}
            </FontIcon>
          </TableRowColumn>

          <TableRowColumn>
            {data.aircraft_skin || ""}
          </TableRowColumn>

          <TableRowColumn>
            {data.nose_art || ""}
          </TableRowColumn>

          <TableRowColumn>
            {data.pilot_skin || ""}
          </TableRowColumn>

          <TableRowColumn>
            {data.spawn_object || ""}
          </TableRowColumn>
        </TableRow>
      );
    });

    return (
      <Table className="table">
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            <TableHeaderColumn
              colSpan="7"
              tooltip="Aircrafts"
              style={{textAlign: "center"}}
            >
              Aircrafts
            </TableHeaderColumn>
          </TableRow>
          <TableRow>
            <TableHeaderColumn>Index</TableHeaderColumn>
            <TableHeaderColumn>Skill</TableHeaderColumn>
            <TableHeaderColumn>Has markings</TableHeaderColumn>
            <TableHeaderColumn>Aircraft skin</TableHeaderColumn>
            <TableHeaderColumn>Nose art</TableHeaderColumn>
            <TableHeaderColumn>Pilot skin</TableHeaderColumn>
            <TableHeaderColumn>Spawn object</TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          {entries}
        </TableBody>
      </Table>
    );
  }

}


class FlightItem extends React.Component {

  render() {
    var data = this.props.data;

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title={"Flight '" + this.props.data.id + "' (" + data.code + ")"}
        />
        <CardText>
          <RaisedButton
            label="View route"
            style={{float: 'right', clear: 'both'}}
            icon={<FontIcon className="material-icons">near_me</FontIcon>}
          />
          <p>
            Air force: <span className={data.air_force.country.belligerent.name}>{data.air_force.verbose_name}</span>
          </p>
          <p>
            Regiment: {
              data.regiment
              ? data.regiment.verbose_name_en
              : "N/A"
            }
          </p>
          <p>
            Squadron index: {data.squadron_index}
          </p>
          <p>
            Flight index: {data.flight_index}
          </p>
          <p>
            Aircraft code: <code>{data.code}</code>
          </p>
          <p>
            Weapons: <code>{data.weapons}</code>
          </p>
          <p>
            Fuel: {data.fuel} %
          </p>
          <Checkbox
            label="Only AI"
            checked={data.ai_only}
            disabled={true}
          />
          <Checkbox
            label="With parachutes"
            checked={data.with_parachutes}
            disabled={true}
          />
          <FlightAircrafts items={data.aircrafts} />
        </CardText>
      </Card>
    );
  }

}

class NoFlights extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Flights" />
        <CardText>
          N/A
        </CardText>
      </Card>
    );
  }

}


export default class Flights extends React.Component {

  render() {
    var self = this
      , list = ((self.props.data || {}).objects || {}).flights || [];

    if (list.length > 0) {
      var nodes = list.map(function(data, i) {
        return (<FlightItem key={i} data={data} />);
      });

      return (<div>{nodes}</div>);
    } else {
      return (<NoFlights />);
    }
  }
}
