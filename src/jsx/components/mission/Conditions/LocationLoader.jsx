import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class LocationLoader extends React.Component {

  render() {
    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="header"
          title="Location loader"
        />
        <CardText>
          <code>
            {
              this.props.value
              ? this.props.value
              : "N/A"
            }
          </code>
        </CardText>
      </Card>
    );
  }

}
