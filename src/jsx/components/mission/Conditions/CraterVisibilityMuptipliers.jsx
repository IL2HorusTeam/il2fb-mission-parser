import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class CraterVisibilityMuptipliers extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Crater visibility muptipliers" />
        <CardText>
          <p>Weapon weight &le; 100 kg: x{this.props.data.le_100kg.toFixed(1)}.</p>
          <p>Weapon weight &le; 1000 kg: x{this.props.data.le_1000kg.toFixed(1)}.</p>
          <p>Weapon weight &gt; 1000 kg: x{this.props.data.gt_1000kg.toFixed(1)}.</p>
        </CardText>
      </Card>
    );
  }

}
