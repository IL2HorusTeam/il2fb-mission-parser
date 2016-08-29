import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class RespawnTime extends React.Component {

  render() {
    var data = this.props.data || {}
      , ships = data.ships || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="mission-details-card-header"
          title="Respawn time"
        />
        <CardText>
          <p>
            Big ships: {
              ships.big !== undefined
              ? ships.big + " sec"
              : "N/A"
            }
          </p>
          <p>
            Small ships: {
              ships.small !== undefined
              ? ships.small + " sec"
              : "N/A"
            }
          </p>
          <p>
            Balloons: {
              data.balloons !== undefined
              ? data.balloons + " sec"
              : "N/A"
            }
          </p>
          <p>
            Artillery: {
              data.artillery !== undefined
              ? data.artillery + " sec"
              : "N/A"
            }
          </p>
          <p>
            Searchlights: {
              data.searchlights !== undefined
              ? data.searchlights + " sec"
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}
