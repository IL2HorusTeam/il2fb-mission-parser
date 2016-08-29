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
    var data = this.props.data || {}
      , conditions = data.conditions || {};

    return (
      <div>
        <LocationLoader
          value={data.location_loader}
        />
        <DateTime
          data={conditions.time_info}
        />
        <Meteorology
          data={conditions.meteorology}
        />
        <HomeBases
          data={conditions.home_bases}
        />
        <Communication
          data={conditions.communication}
        />
        <Radar
          data={conditions.radar}
        />
        <Scouting
          data={conditions.scouting}
        />
        <RespawnTime
          data={conditions.respawn_time}
        />
        <CraterVisibilityMuptipliers
          data={conditions.crater_visibility_muptipliers}
        />
      </div>
    );
  }
}
