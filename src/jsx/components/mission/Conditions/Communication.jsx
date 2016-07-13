import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class Communication extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Communication" />
        <CardText>
          <Checkbox
            label="Tower communication"
            checked={this.props.data.tower_communication}
            disabled={true}
          />
          <Checkbox
            label="Vectoring"
            checked={this.props.data.vectoring}
            disabled={true}
          />
          <Checkbox
            label="Radio silence for AI"
            checked={this.props.data.ai_radio_silence}
            disabled={true}
          />
        </CardText>
      </Card>
    );
  }

}
