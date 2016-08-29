import React from "react";

import {Card, CardHeader, CardText} from 'material-ui/Card';


export default class CraterVisibilityMuptipliers extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="mission-details-card-header"
          title="Crater visibility muptipliers"
        />
        <CardText>
          <p>
            Weapon weight &le; 100 kg: {
              data.le_100kg !== undefined
              ? "×" + data.le_100kg.toFixed(1)
              : "N/A"
            }
          </p>
          <p>
            Weapon weight &le; 1000 kg: {
              data.le_1000kg !== undefined
              ? "×" + data.le_1000kg.toFixed(1)
              : "N/A"
            }
          </p>
          <p>
            Weapon weight &gt; 1000 kg: {
              data.gt_1000kg !== undefined
              ? "×" + data.gt_1000kg.toFixed(1)
              : "N/A"
            }
          </p>
        </CardText>
      </Card>
    );
  }

}
