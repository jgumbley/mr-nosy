var LiteralJSON = React.createClass({
  loadFromServer: function() {
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
  getInitialState: function() {
      return {json: "loading..",
              debug: true };
        },
  componentDidMount: function() {
    this.loadFromServer();
    setInterval(this.loadFromServer, this.props.poll);
  },
  render: function() {
    return (
      <div className="LiteralJSON">
        <div className="checkbox">
            <label>
                <input type='checkbox'
                    onChange={this.onToggleErrorsOnly} 
                    value={this.state.debug} />
                Show debug
            </label>
        </div>
          <code id="language-json">
            {this.state.json}
          </code>
      </div>
    );
  }
});

React.render(
  <LiteralJSON url="api" poll={2000}/>,
  document.getElementById('content')
);


