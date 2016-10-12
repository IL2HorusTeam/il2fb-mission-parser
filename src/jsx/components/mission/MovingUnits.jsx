import React from "react";

import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FontIcon from 'material-ui/FontIcon';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import {Table, TableBody} from 'material-ui/Table';
import {TableHeader, TableHeaderColumn} from 'material-ui/Table';
import {TableRow, TableRowColumn} from 'material-ui/Table';


const SPEED_COEFFICIENT = 3.6;


class ViewUnitRouteButton extends React.Component {

  constructor(props) {
    super(props);
    this.state = {open: false};

    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen() {
    this.setState({open: true});
  }

  handleClose() {
    this.setState({open: false});
  }

  render() {
    const actions = [
      <FlatButton label="Close" primary={true} onTouchTap={this.handleClose}/>
    ];

    var entries = this.props.data.route.map(function(data, i) {
      return (
        <TableRow className="row" hoverable={true} key={i}>
          <TableRowColumn>
            {i}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.x.toFixed(2)}
          </TableRowColumn>

          <TableRowColumn>
            {data.pos.y.toFixed(2)}
          </TableRowColumn>

          <TableRowColumn>
            <FontIcon
              className="material-icons"
              color={data.is_checkpoint ? "green" : "red"}
            >
              {data.is_checkpoint ? "check" : "close"}
            </FontIcon>
          </TableRowColumn>

          <TableRowColumn>
            {data.delay || ""}
          </TableRowColumn>

          <TableRowColumn>
            {data.section_length || ""}
          </TableRowColumn>

          <TableRowColumn>
            {
              data.speed !== null
              ? (data.speed * SPEED_COEFFICIENT).toFixed(2)
              : ""
            }
          </TableRowColumn>
        </TableRow>
      );
    });

    return (
      <div>
        <FlatButton
          label="view"
          labelStyle={{textTransform: 'lowercase', fontWeight: 'normal'}}
          style={{width: '70px', minWidth: '70px'}}
          icon={<FontIcon className="material-icons route">near_me</FontIcon>}
          onTouchTap={this.handleOpen}
        />
        <Dialog
          title={"Route of '" + this.props.data.id + "' (" + this.props.data.code + ")"}
          actions={actions}
          modal={true}
          autoScrollBodyContent={true}
          open={this.state.open}
          onRequestClose={this.handleClose}
          className="dialog"
          bodyStyle={{margin: '1px 0'}}
        >
          <Table className="table">
            <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
              <TableRow>
                <TableHeaderColumn>#</TableHeaderColumn>
                <TableHeaderColumn>X, m</TableHeaderColumn>
                <TableHeaderColumn>Y, m</TableHeaderColumn>
                <TableHeaderColumn>Is checkpoint</TableHeaderColumn>
                <TableHeaderColumn>Delay, min</TableHeaderColumn>
                <TableHeaderColumn>Section length</TableHeaderColumn>
                <TableHeaderColumn>Speed, km/h</TableHeaderColumn>
              </TableRow>
            </TableHeader>
            <TableBody displayRowCheckbox={false} showRowHover={true}>
              {entries}
            </TableBody>
          </Table>
        </Dialog>
      </div>
    );
  }

}


class MovingUnitsGroup extends React.Component {

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
    var key = 0,
        headers = [];

    for (var i = 0; i < this.columns.length; ++i) {
      key++;
      headers.push(
        <TableHeaderColumn key={key}>
          {this.columns[i].title}
        </TableHeaderColumn>
      )
    }

    key++;
    headers.push(
      <TableHeaderColumn key={key}>
        Route
      </TableHeaderColumn>
    );
    return headers;
  }

  renderTableEntry(data, index) {
    var key = 0
      , columns = [];

    for (var i = 0; i < this.columns.length; ++i) {
      var meta = this.columns[i]
        , value = data[meta.attr]
        , handler = meta.handler;

      key++;
      columns.push(handler(value, key));
    }

    key++;
    columns.push(
      <TableRowColumn key={key}>
        <ViewUnitRouteButton data={data} />
      </TableRowColumn>
    );

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

}


class Ships extends MovingUnitsGroup {

  static get defaultProps() {
    return {
      title: "Ships"
    };
  }

  constructor(props) {
    super(props);
    this.columns = this.columns.concat([
      {
          attr: "hibernation"
        , title: "Hibernation"
        , handler: this.renderColumnHibernation
      }, {
          attr: "skill"
        , title: "Skill"
        , handler: this.renderColumnSkill
      }, {
          attr: "recharge_time"
        , title: "Recharge time"
        , handler: this.renderColumnRechargeTime
      }
    ]);
  }

  renderColumnHibernation(value, index) {
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

  renderColumnRechargeTime(value, index) {
    return (
      <TableRowColumn key={index}>
        {value.toFixed(1)}
      </TableRowColumn>
    );
  }

}


class NoMovingUnits extends React.Component {

  render() {
    return (
      <Card className="mission-details-card">
        <CardText>
          Mission has no moving units.
        </CardText>
      </Card>
    );
  }

}


const groupKeyToComponentsMap = {
  ships: Ships
}


export default class MovingUnits extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).moving_units || [];

    if (list.length === 0) {
      return (<NoMovingUnits />);
    }

    var groups = this.groupByType(list)
      , keys = Object.keys(groups);

    keys.sort();

    var children = keys.map(function(key, i) {
      var items = groups[key]
        , Component = groupKeyToComponentsMap[key] || MovingUnitsGroup;

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
