import React from "react";

import {Card, CardTitle} from 'material-ui/Card';


export default class Mission extends React.Component {

  render() {
    if (!this.props.mission) {
      return false;
    }

    return (
      <Card
        className="mission"
      >
        <CardTitle
          title="Mission details"
          subtitle={this.props.mission.file_name}
        />
      </Card>
    )
  }
}
