import React from "react";

import Checkbox from 'material-ui/Checkbox';
import {Card, CardHeader, CardText} from 'material-ui/Card';


class BelligerentScouts extends React.Component {

  render() {
    var listNodes = this.props.items.map(function(item, i) {
      return (<li key={i}>{item}</li>);
    });

    return (
      <Card>
        <CardHeader
          title={"Scouts for " + this.props.belligerent.verbose_name}
        />
        <CardText>
          <ul>
            {listNodes}
          </ul>
        </CardText>
      </Card>
    )
  }

}


class Scouts extends React.Component {

  render() {
    var belligerentScoutsNodes = this.props.data.map(function(data, i) {
      return (
        <BelligerentScouts
          key={i}
          belligerent={data.belligerent}
          items={data.aircrafts}
        />
      );
    });

    return (
      <div>
        {belligerentScoutsNodes}
      </div>
    )
  }

}


export default class Scouting extends React.Component {

  render() {
    return (
      <Card>
        <CardHeader title="Scouting" />
        <CardText>
          <Checkbox
            label="Ships can spot enemy planes with their radars"
            checked={this.props.data.ships_affect_radar}
            disabled={true}
          />
          <Checkbox
            label="Selected scout planes can spot ground units"
            checked={this.props.data.scouts_affect_radar}
            disabled={true}
          />
          <Checkbox
            label="Only scout planes can complete 'recon' targets"
            checked={this.props.data.only_scouts_complete_targets}
            disabled={true}
          />
          <Scouts data={this.props.data.scouts} />
        </CardText>
      </Card>
    );
  }

}
