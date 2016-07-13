import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';



class Wind extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Wind" />
        <CardText>
          <p>Direction: {this.props.data.direction} °</p>
          <p>Speed: {this.props.data.speed} m/s</p>
        </CardText>
      </Card>
    );
  }

}

export default class Meteorology extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Meteorology" />
        <CardText>
          <p>Weather: {this.props.data.weather.verbose_name}</p>
          <p>Gust: {this.props.data.gust.verbose_name}</p>
          <p>Turbulence: {this.props.data.turbulence.verbose_name}</p>
          <p>Cloud base: {this.props.data.cloud_base} m</p>
          <Wind data={this.props.data.wind} />
        </CardText>
      </Card>
    );
  }

}
