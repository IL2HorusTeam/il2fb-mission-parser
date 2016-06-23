import React from "react";

import nl2br from "react-nl2br";
import intersperse from "intersperse";

class FormattedIssue extends React.Component {

  render() {
    if (!this.props.issue) {
      return false;
    }

    return (
      <a href={this.props.issue.url} target='_blank'>
        issue #{this.props.issue.number}
      </a>
    );
  }

}


class RelatedIssue extends React.Component {

  render() {
    if (!this.props.issue) {
      return false;
    }

    return (
      <div>Related issue: <FormattedIssue issue={this.props.issue} />.</div>
    );
  }

}


class SimilarIssues extends React.Component {

  render() {
    if (!this.props.issues || !this.props.issues.length) {
      return false;
    }

    var issues = this.props.issues.map(function(item, index) {
      return <FormattedIssue key={index} issue={item} />;
    })

    return (
      <div>
        Similar issues: {intersperse(issues, ", ")}.
      </div>
    );
  }

}


class FormattedTraceback extends React.Component {

  render() {
    if (!this.props.traceback) {
      return false;
    }

    return (
      <pre className="traceback">
        <code>{this.props.traceback}</code>
      </pre>
    );
  }

}


export default class FormattedError extends React.Component {

  render() {
    if (!this.props.error) {
      return false;
    }

    return (
      <div>
        <div>{nl2br(this.props.error.detail)}</div>
        <RelatedIssue issue={this.props.error.issue} />
        <SimilarIssues issues={this.props.error.similar} />
        <FormattedTraceback traceback={this.props.error.traceback} />
      </div>
    );
  }

}
