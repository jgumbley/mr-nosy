var LiteralJSON = React.createClass({
  getInitialState: function() {
      return {json: "loading.."};
        },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(json) {
        this.setState({json: json});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    return (
      <code className="LiteralJSON" id="language-json">
        {this.state.json}
      </code>
    );
  }
});

React.render(
  <LiteralJSON url="api"/>,
  document.getElementById('content')
);


