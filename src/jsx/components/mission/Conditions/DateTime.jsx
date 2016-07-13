import React from "react";

import DatePicker from 'material-ui/DatePicker';
import FontIcon from 'material-ui/FontIcon';
import TimePicker from 'material-ui/TimePicker';
import {Card, CardHeader, CardText} from 'material-ui/Card';

import dateFormat from "dateformat";


class DateInfo extends React.Component {

  formatDate(value) {
    return dateFormat(value, "mmm dd, yyyy");
  }

  render() {
    var date = new Date(this.props.value);
    return (
        <DatePicker
        floatingLabelText="Date"
        disabled={true}
        value={date}
        formatDate={this.formatDate}
      />
    );
  }

}


class TimeInfo extends React.Component {

  render() {
    var time = new Date()
      , [hours, minutes, seconds] = this.props.value
                                    .match(/(\d+):(\d+):(\d+)/)
                                    .slice(1);

    time.setHours(hours);
    time.setMinutes(minutes);
    time.setSeconds(seconds);

    return (
      <TimePicker
        floatingLabelText="Time"
        format="24hr"
        disabled={true}
        value={time}
      />
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
    return (
      <Card>
        <CardHeader title="Date and time" />
        <CardText>
          <DateInfo value={this.props.data.date} />
          <TimeInfo value={this.props.data.time} />
          <TimeFixationInfo value={this.props.data.is_fixed} />
        </CardText>
      </Card>
    );
  }

}
