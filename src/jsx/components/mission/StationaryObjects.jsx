import React from "react";

import FontIcon from 'material-ui/FontIcon';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


class StationaryObjectsGroup extends React.Component {

  static get defaultProps() {
    return {
      title: "Group title"
    };
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
          attr: "id"
        , title: "ID"
        , handler: this.renderColumnId
      }, {
          attr: "code"
        , title: "Code"
        , handler: this.renderColumnCode
      }, {
          attr: "belligerent"
        , title: "Belligerent"
        , handler: this.renderColumnBelligerent
      }, {
          attr: "pos"
        , title: "X, m"
        , handler: this.renderColumnPosX
      }
      , {
          attr: "pos"
        , title: "Y, m"
        , handler: this.renderColumnPosY
      }
      , {
          attr: "rotation_angle"
        , title: "Angle, °"
        , handler: this.renderColumnRotationAngle
      }
    ];
  }

  render() {
    return (
      <Card className="mission-details-card">
        <CardHeader className="header" title={this.props.title} />
        <CardText>
          {this.renderTable()}
        </CardText>
      </Card>
    );
  }

  renderTable() {
    var self = this
      , headers = self.renderTableHeaders();

    if (self.props.items) {
      var entries = self.props.items.map(function(data, i) {
        return self.renderTableEntry(data, i);
      });
    } else {
      var entries = [
        (
          <TableRow className="row" hoverable={true} key="0">
            <TableRowColumn colspan={this.columns.length + 1}>N/A</TableRowColumn>
          </TableRow>
        )
      ];
    }

    return (
      <Table className="table">
        <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
          <TableRow>
            {headers}
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false} showRowHover={true}>
          {entries}
        </TableBody>
      </Table>
    );
  }

  renderTableHeaders() {
    return this.columns.map(function(meta, i) {
      return (
        <TableHeaderColumn key={i}>
          {meta.title}
        </TableHeaderColumn>
      );
    });
  }

  renderTableEntry(data, index) {
    var columns = this.columns.map(function(meta, i) {
      var value = data[meta.attr]
        , handler = meta.handler;
      return handler(value, i);
    });

    return (
      <TableRow className="row" hoverable={true} key={index}>
        {columns}
      </TableRow>
    );
  }

  renderColumnId(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnCode(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnBelligerent(value, index) {
    return (
      <TableRowColumn key={index} className={value.name}>
        {value.verbose_name}
      </TableRowColumn>
    );
  }

  renderColumnPosX(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.x}
      </TableRowColumn>
    );
  }

  renderColumnPosY(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.y}
      </TableRowColumn>
    );
  }

  renderColumnRotationAngle(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

}


class NoStationaryObjects extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no stationary objects.
        </CardText>
      </Card>
    );
  }

}


class Artillery extends StationaryObjectsGroup {

  static get defaultProps() {
    return {
      title: "Artillery"
    };
  }

  constructor(props) {
    super(props);
    this.columns = this.columns.concat([
      {
          attr: "awakening_time"
        , title: "Awakening time, min"
        , handler: this.renderColumnAwakeningTime
      }, {
          attr: "range"
        , title: "Range, km"
        , handler: this.renderColumnRange
      }, {
          attr: "skill"
        , title: "Skill"
        , handler: this.renderColumnSkill
      }, {
          attr: "use_spotter"
        , title: "Use spotter"
        , handler: this.renderColumnBool
      }
    ]);
  }

  renderColumnAwakeningTime(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnRange(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnSkill(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.verbose_name}
      </TableRowColumn>
    );
  }

  renderColumnBool(value, index) {
    return (
      <TableRowColumn key={index}>
        <FontIcon
          className="material-icons"
          color={value ? "green" : "red"}
        >
          {value ? "check" : "close"}
        </FontIcon>
      </TableRowColumn>
    );
  }

}


class Aircrafts extends StationaryObjectsGroup {

  static get defaultProps() {
    return {
      title: "Aircrafts"
    };
  }

  constructor(props) {
    super(props);
    this.columns = this.columns.concat([
      {
          attr: "air_force"
        , title: "Air force"
        , handler: this.renderColumnAirForce
      }, {
          attr: "skin"
        , title: "Skin"
        , handler: this.renderColumnSkin
      }, {
          attr: "show_markings"
        , title: "Show markings"
        , handler: this.renderColumnBool
      }, {
          attr: "allows_spawning"
        , title: "Allows spawning"
        , handler: this.renderColumnBool
      }, {
          attr: "is_restorable"
        , title: "Is restorable"
        , handler: this.renderColumnBool
      }
    ]);
  }

  renderColumnAirForce(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.verbose_name || "—"}
      </TableRowColumn>
    );
  }

  renderColumnSkin(value, index) {
    return (
      <TableRowColumn key={index}>
        {value || "—"}
      </TableRowColumn>
    );
  }

  renderColumnBool(value, index) {
    return (
      <TableRowColumn key={index}>
        <FontIcon
          className="material-icons"
          color={value ? "green" : "red"}
        >
          {value ? "check" : "close"}
        </FontIcon>
      </TableRowColumn>
    );
  }

}


class Ships extends StationaryObjectsGroup {

  static get defaultProps() {
    return {
      title: "Ships"
    };
  }

  constructor(props) {
    super(props);
    this.columns = this.columns.concat([
      {
          attr: "awakening_time"
        , title: "Awakening time, min"
        , handler: this.renderColumnAwakeningTime
      }, {
          attr: "recharge_time"
        , title: "Recharge time, min"
        , handler: this.renderColumnRechargeTime
      }, {
          attr: "skill"
        , title: "Skill"
        , handler: this.renderColumnSkill
      }
    ]);
  }

  renderColumnAwakeningTime(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnRechargeTime(value, index) {
    return (
      <TableRowColumn key={index}>
        {value}
      </TableRowColumn>
    );
  }

  renderColumnSkill(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.verbose_name}
      </TableRowColumn>
    );
  }

}


const groupKeyToComponentsMap = {
    artillery: Artillery
  , planes: Aircrafts
  , ships: Ships
}


export default class StationaryObjects extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).stationary || [];

    if (list.length === 0) {
        return (<NoStationaryObjects />);
    }

    var groups = this.groupByType(list)
      , keys = Object.keys(groups);

    keys.sort();

    var children = keys.map(function(key, i) {
      var items = groups[key]
        , Component = groupKeyToComponentsMap[key] || StationaryObjectsGroup;

      return (<Component title={key} items={items} key={i} />);
    });

    return <div>{children}</div>;
  }

  groupByType(list) {
    var groups = {};

    for (var i = 0; i < list.length; ++i) {
      var item = list[i]
        , type_key = item.type.value;

      if (type_key in groups)
        groups[type_key].push(item);
      else {
        groups[type_key] = [item];
      }
    }

    return groups;
  }

}
