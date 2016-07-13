import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


class ShipsGroup extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title={this.props.title} />
        <CardText>
          <p>Max range: {this.props.data.max_range} km</p>
          <p>Min height: {this.props.data.min_height} m</p>
          <p>Max height: {this.props.data.max_height} m</p>
        </CardText>
      </Card>
    )
  }

}


class Ships extends React.Component {

  render() {
    return (
      <div>
        <ShipsGroup
          title="Big ships"
          data={this.props.data.big}
        />
        <ShipsGroup
          title="Small ships"
          data={this.props.data.small}
        />
      </div>
    )
  }

}


class Scouts extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Scouts" />
        <CardText>
          <p>Max range: {this.props.data.max_range} km</p>
          <p>Max height: {this.props.data.max_height} m</p>
          <p>&alpha; angle: {this.props.data.alpha} °</p>
        </CardText>
      </Card>
    )
  }

}


export default class Radar extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Radar settings" />
        <CardText>
          <Checkbox
            label="Radar is in advanced mode"
            checked={this.props.data.advanced_mode}
            disabled={true}
          />
          <p>Refresh interval: {this.props.data.refresh_interval} sec</p>
          <Ships data={this.props.data.ships} />
          <Scouts data={this.props.data.scouts} />
        </CardText>
      </Card>
    );
  }

}
