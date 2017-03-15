import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';



class Wind extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card sub"
      >
        <CardHeader
          className="header"
          title="Wind"
        />
        <CardText>
          <p>
            Direction: {
              data.direction !== undefined
              ? data.direction.toFixed(1) + " °"
              : "N/A"
            }
          </p>
          <p>
            Speed: {
              data.speed !== undefined
              ? data.speed.toFixed(1) + " m/s"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}

export default class Meteorology extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="header"
          title="Meteorology"
        />
        <CardText>
          <p>
            Weather: {
              data.weather
              ? data.weather.verbose_name
              : "N/A"
            }
          </p>
          <p>
            Gust: {
              data.gust
              ? data.gust.verbose_name
              : "N/A"
            }
          </p>
          <p>
            Turbulence: {
              data.turbulence
              ? data.turbulence.verbose_name
              : "N/A"
            }
          </p>
          <p>
            Cloud base: {
              data.cloud_base !== undefined
              ? data.cloud_base + " m"
              : "N/A"
            }
          </p>
          <Wind data={data.wind} />
        </CardText>
      </Card>
    );
  }

}
