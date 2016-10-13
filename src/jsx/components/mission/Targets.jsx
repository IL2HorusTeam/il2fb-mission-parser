import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';
import Checkbox from 'material-ui/Checkbox';


class Position2DCard extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title="Position"
        />
        <CardText>
          <p>
            X: {
              data.x !== undefined
              ? data.x.toFixed(2) + " m"
              : "N/A"
            }
          </p>
          <p>
            Y: {
              data.y !== undefined
              ? data.y.toFixed(2) + " m"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}

class TargetObject extends React.Component {

  render() {
    var data = this.props.data || {}
      , children = [];

    children.push(
      <p>ID: <code>{data.id}</code></p>
    );

    if (data.waypoint !== undefined) {
      children.push(
        <p>Waypoint: #{data.waypoint}</p>
      );
    }

    children.push(
      <Position2DCard data={data.pos} />
    );

    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title="Object" />
        <CardText>
          {children}
        </CardText>
      </Card>
    );
  }

}


class TargetItem extends React.Component {

  render() {
    var data = this.props.data || {}
      , children = [];

    children.push(
      <p>Type: {data.type.verbose_name}</p>
    );

    children.push(
      <p>Priority: {data.priority.verbose_name}</p>
    );

    children.push(
      <p>Delay: {data.delay} min</p>
    );

    if (data.radius !== undefined) {
      children.push(
        <p>Radius: {data.radius} m</p>
      );
    }

    if (data.destruction_level !== undefined) {
      children.push(
        <p>Destruction level: {data.destruction_level} %</p>
      );
    }

    children.push(
      <Checkbox
        label="In sleep mode"
        checked={data.in_sleep_mode}
        disabled={true}
      />
    );

    if (data.requires_landing !== undefined) {
      children.push(
        <Checkbox
          label="Requires landing"
          checked={data.requires_landing}
          disabled={true}
        />
      );
    }

    children.push(
      <Position2DCard data={data.pos} />
    );

    if (data.object !== undefined) {
      children.push(
        <TargetObject data={data.object} />
      );
    }

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title={"Target #" + this.props.index}
        />
        <CardText>
          {children}
        </CardText>
      </Card>
    );
  }

}


class NoTargets extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no targets.
        </CardText>
      </Card>
    );
  }

}


export default class Targets extends React.Component {

  render() {
    var items = (this.props.data || {}).targets || [];

    if (items.length === 0) {
      return (<NoTargets />);
    }

    var children = items.map(function(data, i) {
      return (<TargetItem key={i} index={i} data={data} />);
    });

    return (<div>{children}</div>);
  }
}
