var DebugPanel = React.createClass({
    render: function() { return (
      <pre id="language-html">
        {this.props.json}
      </pre>
    )}
});

var ToggleDebugPanelCheckbox = React.createClass({
    handleChange: function(e) { 
        this.props.onUpdate(this.props.checked);

    },
    render: function() { return (
        <div className="checkbox">
            <label>
                <input type='checkbox'
                    onChange={this.handleChange} 
                    checked={this.props.checked} />
                Show debug
            </label>
        </div>
    )}
});

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
      return {json: {data: { radios:[] },
              debug: false }};
  },
  handleUpdateDebugState: function(currentState) {
      this.setState({ debug: !( currentState ) });
  },
  componentDidMount: function() {
    this.loadFromServer();
    setInterval(this.loadFromServer, this.props.poll);
  },
  render: function() {
    return (
      <div className="LiteralJSON">
        <D3Chart width={1920} height={1080} data={this.state.json.data.radios}/>
        <ToggleDebugPanelCheckbox checked={this.state.debug} onUpdate={this.handleUpdateDebugState} />
        { this.state.debug ? (
            <DebugPanel json={JSON.stringify(this.state.json, null, 2)}/>
            ): null
        }
      </div>
    );
  }
});

var D3Chart = React.createClass({
  render: function() {
    return (
      <div className="D3Chart">
      </div>
    );
    },
   componentDidUpdate: function() {
   /* Seems not unreasonable to have the D3 initialise in here
    */
        this.updateD3();
    },
   componentDidMount: function() {
   /* Seems not unreasonable to have the D3 initialise in here
    */
        this.svg = d3.select(this.getDOMNode()).append("svg");
        this.svg
            .attr("width", this.props.width)
            .attr("height", this.props.height);
       
        this.force = d3.layout.force()
            .charge(-220)
            .size([this.props.width, this.props.height]);

        this.updateD3();
    },
    reconcileNodes: function(currentNodes, updatedNodes) {
        /* reconcile any nodes which are already being displayed with the ones already in the force
         directed layout so that x, y position are retained
         */
        var currentNodesByKey = currentNodes.reduce(
            function(acc, item) { acc[item.name] = item; return acc; }, {}
        );

        function keyNotAlreadyIn(name) {return typeof currentNodesByKey[name] === 'undefined'}

        return updatedNodes.map(
            function (node) {
                if (keyNotAlreadyIn(node.name)) {
                    return node;
                } else {
                    return currentNodesByKey[node.name];
                }
            }
        );
    },
   updateD3: function() {
        this.force.nodes(
            this.reconcileNodes(
                this.force.nodes(),
                this.props.data
            )
        );

        this.circleJoin = this.svg.selectAll("circle")
                .data(this.force.nodes(), 
                      function(d) { 
                        return d.name; }
                      );

        this.circleJoin.enter().append("circle")
                .attr("r", 30)
                .call(this.force.drag());

        this.circleJoin.exit().remove();

        this.force.on('tick', function() {
            this.circleJoin.attr('cx', function(d) { return d.x; })
                .attr('cy', function(d) { return d.y; });
        }.bind(this));

        this.force.start();
        
   }
});

React.render(
  <LiteralJSON url="api/all_radios" poll={2000}/>,
  document.getElementById('content')
);


