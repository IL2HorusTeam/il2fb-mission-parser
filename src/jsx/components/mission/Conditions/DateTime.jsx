import React from "react";

import FontIcon from 'material-ui/FontIcon';
import {Card, CardHeader, CardText} from 'material-ui/Card';

import dateFormat from "dateformat";


class DateInfo extends React.Component {

  render() {
    return (
      <p>
        Date: {
          this.props.value
          ? dateFormat(this.props.value, "mmm dd, yyyy")
          : "N/A"
        }
      </p>
    );
  }

}


class TimeInfo extends React.Component {

  render() {
    return (
      <p>
        Time: {
          this.props.value
          ? this.props.value
          : "N/A"
        }
      </p>
    );
  }

}


class TimeFixationInfo extends React.Component {

  render() {
    return (
      <div>
        <FontIcon className="material-icons fixation">
          {
            this.props.value
            ? "lock_outline"
            : "lock_open"
          }
        </FontIcon>
        {
          this.props.value
          ? "Time is fixed"
          : "Time is not fixed"
        }
      </div>
    );
  }

}


export default class DateTime extends React.Component {

  render() {
    var data = this.props.data || {};

    return (
      <Card
        className="mission-details-card"
      >
        <CardHeader
          className="header"
          title="Date and time"
        />
        <CardText>
          <DateInfo value={data.date} />
          <TimeInfo value={data.time} />
          <TimeFixationInfo value={data.is_fixed} />
        </CardText>
      </Card>
    );
  }

}
