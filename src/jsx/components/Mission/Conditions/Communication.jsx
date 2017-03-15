import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class Communication extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card className="mission-details-card">
        <CardHeader
          className="header"
          title="Communication"
        />
        <CardText>
          <Checkbox
            label="Tower communication"
            checked={data.tower_communication}
            disabled={true}
          />
          <Checkbox
            label="Vectoring"
            checked={data.vectoring}
            disabled={true}
          />
          <Checkbox
            label="Radio silence for AI"
            checked={data.ai_radio_silence}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}
