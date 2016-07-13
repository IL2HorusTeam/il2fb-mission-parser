import React from "react";

import Communication from './Communication';
import CraterVisibilityMuptipliers from './CraterVisibilityMuptipliers';
import DateTime from './DateTime';
import HomeBases from './HomeBases';
import LocationLoader from './LocationLoader';
import Meteorology from './Meteorology';
import Radar from './Radar';
import RespawnTime from './RespawnTime';
import Scouting from './Scouting';

export default class Conditions extends React.Component {

  render() {
    return (
      <div>
        <LocationLoader
          value={this.props.data.location_loader}
        />
        <DateTime
          data={this.props.data.conditions.time_info}
        />
        <Meteorology
          data={this.props.data.conditions.meteorology}
        />
        <HomeBases
          data={this.props.data.conditions.home_bases}
        />
        <Communication
          data={this.props.data.conditions.communication}
        />
        <Radar
          data={this.props.data.conditions.radar}
        />
        <Scouting
          data={this.props.data.conditions.scouting}
        />
        <RespawnTime
          data={this.props.data.conditions.respawn_time}
        />
        <CraterVisibilityMuptipliers
          data={this.props.data.conditions.crater_visibility_muptipliers}
        />
      </div>
    );
  }
}
