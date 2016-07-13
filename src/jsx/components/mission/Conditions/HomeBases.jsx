import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class HomeBases extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Home bases" />
        <CardText>
          <Checkbox
            label="Hide AI aircrafts after landing"
            checked={this.props.data.hide_ai_aircrafts_after_landing}
            disabled={true}
          />
          <Checkbox
            label="Hide hostile and unpopulated airfields"
            checked={this.props.data.hide_unpopulated}
            disabled={true}
          />
          <Checkbox
            label="Hide number of players"
            checked={this.props.data.hide_players_count}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}
