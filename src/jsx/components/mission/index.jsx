import React from "react";
import update from "react-addons-update";

import {Card, CardTitle} from 'material-ui/Card';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';

import Buildings from './Buildings';
import Cameras from './Cameras';
import Flights from './Flights';
import GeneralInfo from './GeneralInfo';
import HomeBases from './HomeBases';
import Markers from './Markers';
import MovingUnits from './MovingUnits';
import PlayerInfo from './PlayerInfo';
import Rockets from './Rockets';
import StationaryObjects from './StationaryObjects';
import Targets from './Targets';


const tabs_to_components_map = {
  'buildings': Buildings,
  'cameras': Cameras,
  'flights': Flights,
  'generalInfo': GeneralInfo,
  'homeBases': HomeBases,
  'markers': Markers,
  'movingUnits': MovingUnits,
  'playerInfo': PlayerInfo,
  'rockets': Rockets,
  'stationaryObjects': StationaryObjects,
  'targets': Targets,
}


export default class Mission extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      activeTab: 'generalInfo'
    };

    this.handleMenuItemSelected = this.handleMenuItemSelected.bind(this);
  }

  handleMenuItemSelected(event, menuItem, index) {
    this.setState(update(this.state, {$merge: {
      activeTab: menuItem.props.value
    }}));
  }

  render() {
    if (!this.props.mission) {
      return false;
    }

    var Details = tabs_to_components_map[this.state.activeTab];

    return (
      <Card className="mission-details-pane">
        <CardTitle
          title="Mission details"
          subtitle={this.props.mission.file_name}
        />

        <div className="mission-details">
          <div className="mission-details-menu">
            <Menu
              value={this.state.activeTab}
              onItemTouchTap={this.handleMenuItemSelected}
            >
              <MenuItem
                primaryText="General info"
                value="generalInfo"
              />
              <MenuItem
                primaryText="Player info"
                value="playerInfo"
              />
              <MenuItem
                primaryText="Moving units"
                value="movingUnits"
              />
              <MenuItem
                primaryText="Flights"
                value="flights"
              />
              <MenuItem
                primaryText="Home bases"
                value="homeBases"
              />
              <MenuItem
                primaryText="Stationary objects"
                value="stationaryObjects"
              />
              <MenuItem
                primaryText="Buildings"
                value="buildings"
              />
              <MenuItem
                primaryText="Rockets"
                value="rockets"
              />
              <MenuItem
                primaryText="Targets"
                value="targets"
              />
              <MenuItem
                primaryText="Cameras"
                value="cameras"
              />
              <MenuItem
                primaryText="Markers"
                value="markers"
              />
            </Menu>
          </div>

          <div className="mission-details-data">
            <Details data={this.props.mission.data}/>
          </div>
        </div>
      </Card>
    )
  }
}
