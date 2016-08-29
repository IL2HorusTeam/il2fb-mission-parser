import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class HomeBases extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="mission-details-card-header"
          title="Home bases"
        />
        <CardText>
          <Checkbox
            label="Hide AI aircrafts after landing"
            checked={data.hide_ai_aircrafts_after_landing}
            disabled={true}
          />
          <Checkbox
            label="Hide hostile and unpopulated airfields"
            checked={data.hide_unpopulated}
            disabled={true}
          />
          <Checkbox
            label="Hide number of players"
            checked={data.hide_players_count}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}
