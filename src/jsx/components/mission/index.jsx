import React from "react";
import update from "react-addons-update";

import {Card, CardTitle} from 'material-ui/Card';
import {List, ListItem, MakeSelectable} from 'material-ui/List';

import Buildings from './Buildings';
import Cameras from './Cameras';
import Flights from './Flights';
import Conditions from './Conditions';
import HomeBases from './HomeBases';
import Markers from './Markers';
import MovingUnits from './MovingUnits';
import PlayerInfo from './PlayerInfo';
import Rockets from './Rockets';
import StationaryObjects from './StationaryObjects';
import Targets from './Targets';


let SelectableList = MakeSelectable(List);

const tabsToComponentsMap = {
  buildings: Buildings,
  cameras: Cameras,
  conditions: Conditions,
  flights: Flights,
  homeBases: HomeBases,
  markers: Markers,
  movingUnits: MovingUnits,
  playerInfo: PlayerInfo,
  rockets: Rockets,
  stationaryObjects: StationaryObjects,
  targets: Targets,
}


export default class Mission extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      activeTab: 'conditions'
    };

    this.handleListItemSelected = this.handleListItemSelected.bind(this);
  }

  handleListItemSelected(event, value) {
    this.setState(update(this.state, {$merge: {
      activeTab: value
    }}));
  }

  render() {
    if (!this.props.mission) {
      return false;
    }

    var Details = tabsToComponentsMap[this.state.activeTab];

    return (
      <Card className="mission-details-pane">
        <CardTitle
          title="Mission details"
          subtitle={this.props.mission.file_name}
        />

        <div className="mission-details">
          <div className="mission-details-menu">
            <SelectableList
              value={this.state.activeTab}
              onChange={this.handleListItemSelected}
            >
              <ListItem
                primaryText="Conditions"
                value="conditions"
              />
              <ListItem
                primaryText="Player info"
                value="playerInfo"
              />
              <ListItem
                primaryText="Moving units"
                value="movingUnits"
              />
              <ListItem
                primaryText="Flights"
                value="flights"
              />
              <ListItem
                primaryText="Home bases"
                value="homeBases"
              />
              <ListItem
                primaryText="Stationary objects"
                value="stationaryObjects"
              />
              <ListItem
                primaryText="Buildings"
                value="buildings"
              />
              <ListItem
                primaryText="Rockets"
                value="rockets"
              />
              <ListItem
                primaryText="Targets"
                value="targets"
              />
              <ListItem
                primaryText="Cameras"
                value="cameras"
              />
              <ListItem
                primaryText="Markers"
                value="markers"
              />
            </SelectableList>
          </div>

          <div className="mission-details-data">
            <Details data={this.props.mission.data} />
          </div>
        </div>
      </Card>
    );
  }
}
