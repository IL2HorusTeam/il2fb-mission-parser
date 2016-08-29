import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


class ShipsGroup extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card sub"
      >
        <CardHeader
          className="mission-details-card-header"
          title={this.props.title || "N/A"}
        />
        <CardText>
          <p>
            Max range: {
              data.max_range !== undefined
              ? data.max_range + " km"
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
    )
  }

}


class Ships extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <div>
        <ShipsGroup
          title="Big ships"
          data={data.big}
        />
        <ShipsGroup
          title="Small ships"
          data={data.small}
        />
      </div>
    )
  }

}


class Scouts extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card sub"
      >
        <CardHeader
          className="mission-details-card-header"
          title="Scouts"
        />
        <CardText>
          <p>
            Max range: {
              data.max_range !== undefined
              ? data.max_range + " km"
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
          <p>
            &alpha; angle: {
              data.alpha !== undefined
              ? data.alpha + " °"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    )
  }

}


export default class Radar extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="mission-details-card-header"
          title="Radar settings"
        />
        <CardText>
          <Checkbox
            label="Radar is in advanced mode"
            checked={data.advanced_mode}
            disabled={true}
          />
          <p>
            Refresh interval: {
              data.refresh_interval !== undefined
              ? data.refresh_interval + " sec"
              : "N/A"
            }
          </p>
          <Ships
            data={data.ships}
          />
          <Scouts
            data={data.scouts}
          />
        </CardText>
      </Card>
    );
  }

}
