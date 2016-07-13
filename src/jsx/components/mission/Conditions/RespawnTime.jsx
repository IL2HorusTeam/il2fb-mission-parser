import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class RespawnTime extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Respawn time" />
        <CardText>
          <p>Big ships: {this.props.data.ships.big} sec.</p>
          <p>Small ships: {this.props.data.ships.small} sec.</p>
          <p>Balloons: {this.props.data.balloons} sec.</p>
          <p>Artillery: {this.props.data.artillery} sec.</p>
          <p>Searchlights: {this.props.data.searchlights} sec.</p>
        </CardText>
      </Card>
    );
  }

}
