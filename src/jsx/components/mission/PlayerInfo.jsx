import React from "react";

import FontIcon from 'material-ui/FontIcon';
import {Card, CardText} from 'material-ui/Card';


class WeaponsFixationInfo extends React.Component {

  render() {
    return (
      <div>
        <FontIcon className="material-icons fixation">
          {
            this.props.value
            ? "lock_outline"
            : "lock_open"
          }
        </FontIcon>
        {
          this.props.value
          ? "Weapons are fixed"
          : "Weapons are not fixed"
        }
      </div>
    );
  }

}


export default class PlayerInfo extends React.Component {

  render() {
    var data = (this.props.data || {}).player || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardText>
          <p>
            Belligerent: {
              data.belligerent
              ? data.belligerent.verbose_name
              : "N/A"
            }
          </p>
          <p>
            Flight ID: {
              (data.flight_id !== undefined) && (data.flight_id !== null)
              ? data.flight_id
              : "N/A"
            }
          </p>
          <p>
            Aircraft index: {
              data.aircraft_index !== undefined
              ? data.aircraft_index
              : "N/A"
            }
          </p>
          <WeaponsFixationInfo
            value={data.fixed_weapons}
          />
        </CardText>
      </Card>
    )
  }
}
