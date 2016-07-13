import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class LocationLoader extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Location loader" />
        <CardText>
          <code>{this.props.value}</code>
        </CardText>
      </Card>
    );
  }

}
