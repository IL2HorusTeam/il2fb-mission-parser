import React, {PropTypes} from "react";
import update from "react-addons-update";

import {Card, CardTitle} from 'material-ui/Card';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';


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

    return (
      <Card className="mission">
        <CardTitle
          title="Mission details"
          subtitle={this.props.mission.file_name}
        />

        <div>
          <div className="menu">
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
                primaryText="Static objects"
                value="staticObjects"
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
        </div>
      </Card>
    )
  }
}
