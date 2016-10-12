import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {List, ListItem} from 'material-ui/List';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class GeneralInfo extends React.Component {

  render() {
    var data = this.props.data;

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="General info" />
        <CardText>
          <p>
            Belligerent: {
              data.belligerent
              ? <span className={data.belligerent.name}>{data.belligerent.verbose_name}</span>
              : "N/A"
            }
          </p>
          <p>
            Range: {
              data.range !== undefined
              ? data.range
              : "N/A"
            }
          </p>
          <Checkbox
            label="Show default icon"
            checked={data.show_default_icon}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}


class Position extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Position" />
        <CardText>
          <p>
            X: {
              data.x !== undefined
              ? data.x.toFixed(2)
              : "N/A"
            }
          </p>
          <p>
            Y: {
              data.y !== undefined
              ? data.y.toFixed(2)
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}


class Friction extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Friction" />
        <CardText>
          <Checkbox
            label="Enabled"
            checked={data.enabled}
            disabled={true}
          />
          <p>
            Value: {
              data.value !== undefined
              ? data.value.toFixed(1)
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}


class Radar extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Radar" />
        <CardText>
          <p>
            Range: {
              data.range !== undefined
              ? data.range + " km"
              : "N/A"
            }
          </p>
          <p>
            Min height: {
              data.min_height !== undefined
              ? data.min_height + " m"
              : "N/A"
            }
          </p>
          <p>
            Max height: {
              data.max_height !== undefined
              ? data.max_height + " m"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}


class SpawningInAir extends React.Component {

  render() {
    var data = this.props.data || {}
      , conditions = data.conditions || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="In air" />
        <CardText>
          <Checkbox
            label="Always spawn in air"
            checked={conditions.always}
            disabled={true}
          />
          <Checkbox
            label="Spawn in air if deck is full"
            checked={conditions.if_deck_is_full}
            disabled={true}
          />
          <p>
            Height: {
              data.height !== undefined
              ? data.height + " m"
              : "N/A"
            }
          </p>
          <p>
            Speed: {
              data.speed !== undefined
              ? data.speed + " km/h"
              : "N/A"
            }
          </p>
          <p>
            Heading: {
              data.heading !== undefined
              ? data.heading + " °"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}


class SpawningInStationary extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="In stationary" />
        <CardText>
          <Checkbox
            label="Enabled"
            checked={data.enabled}
            disabled={true}
          />
          <Checkbox
            label="Return aircrafts to start position"
            checked={data.return_to_start_position}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}


class SpawningAllowedAirForces extends React.Component {

  render() {
    var items = this.props.data || {},
        body = this.getBody(items);

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Allowed air forces" />
        <CardText>
          {body}
        </CardText>
      </Card>
    );
  }

  getBody(items) {
    if (items.length === 0) {
      return (
        <p>All air forces are allowed.</p>
      );
    }

    var listItems = items.map(function(item, i) {
      return (
        <ListItem
          key={i}
          primaryText={item.verbose_name}
          title={
            item.help_text
            ? item.help_text
            : null
          }
        />
      );
    });

    return (
      <List children={listItems} />
    );
  }

}


class SpawningAircraftLimitations extends React.Component {

  render() {
    var self = this
      , data = this.props.data || {}
      , allowed_aircrafts = data.allowed_aircrafts || [];

    if (allowed_aircrafts.length) {
      var entries = allowed_aircrafts.map(function(data, i) {
        return self.renderTableEntry(data, i);
      });
    } else {
      var entries = [
        this.renderEmptyTableEntry()
      ];
    }

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Aircraft limitations" />
        <CardText>
          <Checkbox
            label="Enabled"
            checked={data.enabled}
            disabled={true}
          />
          <Checkbox
            label="Loses planes as they get destroyed"
            checked={data.consider_lost}
            disabled={true}
          />
          <Checkbox
            label="Loses planes as static aircrafts get destroyed"
            checked={data.consider_stationary}
            disabled={true}
          />
          <Table className="table">
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn colSpan="3" style={{textAlign: "center"}}>
                  Allowed aircrafts
                </TableHeaderColumn>
              </TableRow>
              <TableRow>
                <TableHeaderColumn>Code</TableHeaderColumn>
                <TableHeaderColumn>Limit</TableHeaderColumn>
                <TableHeaderColumn>Weapon limitations</TableHeaderColumn>
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

  renderEmptyTableEntry() {
    return (
      <TableRow className="row" hoverable={true} key="0">
        <TableRowColumn colspan="3">
          All aircrafts are allowed.
        </TableRowColumn>
      </TableRow>
    );
  }

  renderTableEntry(data, index) {
    return (
      <TableRow className="row" hoverable={true} key={index}>
        <TableRowColumn>
          {data.code}
        </TableRowColumn>
        <TableRowColumn>
          {
            data.limit !== null
            ? data.limit
            : "no limit"
          }
        </TableRowColumn>
        <TableRowColumn>
          {
            data.weapon_limitations.join(",") || "no limitations"
          }
        </TableRowColumn>
      </TableRow>
    );
  }

}


class Spawning extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Spawning" />
        <CardText>
          <Checkbox
            label="Enabled"
            checked={data.enabled}
            disabled={true}
          />
          <Checkbox
            label="With parachutes"
            checked={data.with_parachutes}
            disabled={true}
          />
          <p>
            Max pilots: {
              data.max_pilots !== undefined
              ? data.max_pilots
              : "N/A"
            }
          </p>
          <SpawningInAir data={data.in_air} />
          <SpawningInStationary data={data.in_stationary} />
          <SpawningAllowedAirForces data={data.allowed_air_forces} />
          <SpawningAircraftLimitations data={data.aircraft_limitations} />
        </CardText>
      </Card>
    );
  }

}


class HomeBaseItem extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title={"Home base #" + this.props.index}
        />
        <CardText>
          <GeneralInfo data={data} />
          <Position data={data.pos} />
          <Friction data={data.friction} />
          <Radar data={data.radar} />
          <Spawning data={data.spawning} />
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
