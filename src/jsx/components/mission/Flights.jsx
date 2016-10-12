import React from "react";

import Checkbox from 'material-ui/Checkbox';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FontIcon from 'material-ui/FontIcon';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class RoutePointOptions extends React.Component {

  render() {
    var data = this.props.data;

    if (data.delay === undefined && data.patrol_cycles === undefined) {
      return false;
    }

    var fields = [];

    if (data.patrol_cycles !== undefined) {
      fields.push(
        <p>Patrol cycles: {data.patrol_cycles}</p>
      );
    }

    if (data.patrol_timeout !== undefined) {
      fields.push(
        <p>Patrol timeout: {data.patrol_timeout} min</p>
      );
    }

    if (data.delay !== undefined) {
      fields.push(
        <p>Delay: {data.delay} min</p>
      );
    }

    if (data.spacing !== undefined) {
      fields.push(
        <p>Spacing: {data.spacing} m</p>
      );
    }

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Options" />
        <CardText>
          {fields}
        </CardText>
      </Card>
    );
  }

}


class RoutePointPattern extends React.Component {

  render() {
    var data = this.props.data;

    if (data.pattern_angle === undefined) {
      return false;
    }

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Pattern" />
        <CardText>
          <p>Angle: {data.pattern_angle} °</p>
          <p>Side size: {data.pattern_side_size} km</p>
          <p>Altitude difference: {data.pattern_altitude_difference} m</p>
        </CardText>
      </Card>
    );
  }

}


class RoutePointTarget extends React.Component {

  render() {
    var data = this.props.data;

    if (data.target_id === undefined) {
      return false;
    }

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Target" />
        <CardText>
          <p>Target ID: <code>{data.target_id}</code></p>
          <p>Index of target's route point: {data.target_route_point}</p>
        </CardText>
      </Card>
    );
  }

}


class RoutePointExtraButton extends React.Component {

  constructor(props) {
    super(props);
    this.state = {open: false};

    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen() {
    this.setState({open: true});
  }

  handleClose() {
    this.setState({open: false});
  }

  render() {
    var data = this.props.data;

    if (
      data.delay === undefined
      && data.patrol_cycles === undefined
      && data.target_id === undefined
    ) {
      return false;
    }

    const actions = [
      <FlatButton label="Close" primary={true} onTouchTap={this.handleClose}/>
    ];

    return (
      <div>
        <FlatButton
          icon={<FontIcon className="material-icons">info_outline</FontIcon>}
          onTouchTap={this.handleOpen}
          style={{width: '40px', minWidth: '40px'}}
        />
        <Dialog
          title={"Extra info about route point #" + this.props.index}
          actions={actions}
          modal={true}
          autoScrollBodyContent={true}
          open={this.state.open}
          onRequestClose={this.handleClose}
          className="dialog"
          bodyStyle={{margin: '15px 0 1px'}}
        >
          <RoutePointOptions data={data} />
          <RoutePointPattern data={data} />
          <RoutePointTarget data={data} />
        </Dialog>
      </div>
    );
  }

}


class FlightRoute extends React.Component {

  render() {
    var rows = this.props.items.map(function(data, i) {
      return (
        <TableRow className="row" hoverable={true} key={i}>
          <TableRowColumn>
            {i}
          </TableRowColumn>

          <TableRowColumn>
            {data.type.verbose_name}
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

          <TableRowColumn>
            {data.speed}
          </TableRowColumn>

          <TableRowColumn>
            {data.formation ? data.formation.verbose_name : "default"}
          </TableRowColumn>

          <TableRowColumn>
            <FontIcon
              className="material-icons"
              color={data.radio_silence ? "green" : "red"}
            >
              {data.radio_silence ? "check" : "close"}
            </FontIcon>
          </TableRowColumn>

          <TableRowColumn>
            <RoutePointExtraButton
              data={data}
              index={i}
            />
          </TableRowColumn>

        </TableRow>
      );
    });

    return (
      <Table className="table">
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            <TableHeaderColumn>#</TableHeaderColumn>
            <TableHeaderColumn>Type</TableHeaderColumn>
            <TableHeaderColumn>X, m</TableHeaderColumn>
            <TableHeaderColumn>Y, m</TableHeaderColumn>
            <TableHeaderColumn>Z, m</TableHeaderColumn>
            <TableHeaderColumn>Speed, km/h</TableHeaderColumn>
            <TableHeaderColumn>Formation</TableHeaderColumn>
            <TableHeaderColumn>Radio silence</TableHeaderColumn>
            <TableHeaderColumn>Extra</TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          {rows}
        </TableBody>
      </Table>
    );
  }

}


class ViewFlightRouteButton extends React.Component {

  constructor(props) {
    super(props);
    this.state = {open: false};

    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen() {
    this.setState({open: true});
  }

  handleClose() {
    this.setState({open: false});
  }

  render() {
    const actions = [
      <FlatButton
        label="Close"
        primary={true}
        onTouchTap={this.handleClose}
      />,
    ];

    return (
      <div style={this.props.style}>
        <RaisedButton
          label="View route"
          icon={<FontIcon className="material-icons">near_me</FontIcon>}
          onTouchTap={this.handleOpen}
        />
        <Dialog
          title={"Route of '" + this.props.data.id + "' (" + this.props.data.code + ")"}
          actions={actions}
          modal={true}
          autoScrollBodyContent={true}
          open={this.state.open}
          onRequestClose={this.handleClose}
          className="dialog"
          bodyStyle={{margin: '1px 0'}}
        >
          <FlightRoute items={this.props.data.route} />
        </Dialog>
      </div>
    );
  }

}


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
            <TableHeaderColumn colSpan="7" style={{textAlign: "center"}}>
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
          <ViewFlightRouteButton
            style={{float: 'right', clear: 'both'}}
            data={data}
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
        <CardText>
          Mission has no flights.
        </CardText>
      </Card>
    );
  }

}


export default class Flights extends React.Component {

  render() {
    var items = ((this.props.data || {}).objects || {}).flights || [];

    if (items.length > 0) {
      var children = items.map(function(data, i) {
        return (<FlightItem key={i} data={data} />);
      });

      return (<div>{children}</div>);
    } else {
      return (<NoFlights />);
    }
  }

}
