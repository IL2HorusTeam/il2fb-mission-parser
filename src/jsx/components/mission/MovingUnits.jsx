import React from "react";


export default class MovingUnits extends React.Component {

  render() {
    var list = ((this.props.data || {}).objects || {}).moving_units || []
      , groups = this.group_by_type(list);

    return (
      <div>Moving units</div>
    )
  }

  group_by_type(list) {
    var groups = {};

    for (var i = 0; i < list.length; ++i) {
      var item = list[i]
        , type_name = item.type.name;

      if (type_name in list)
        groups[type_name].items.push(item);
      else {
        groups[type_name] = {
            items: [item]
          , type: item.type
        };
      }

      delete item.type;
    }

    return groups;
  }
}
