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

       this.svg.append("g").attr("id", "links");
       this.svg.append("g").attr("id", "nodes");
       
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
       /* obviously this is a heuristic at best */
       if (this.force.nodes().length != this.props.data.length) {
           this.processUpdate();
       };
   },
   processUpdate: function() {
        var nodes = this.reconcileNodes(
                this.force.nodes(),
                this.props.data
            );

       var currentNodesByKey = nodes.reduce(
           function(acc, item) { acc[item.name] = item; return acc; }, {}
       );


        var links = nodes
                    .filter( function (node) { return !(node.ap) })
                    .filter( function (node) { return "assoc_with" in node })
                    .map( function (node) {
                        var target = currentNodesByKey[node.name];
                        var source = currentNodesByKey[node.assoc_with];
                        return {source: source, target: target};
            });

       this.force
           .nodes(nodes);

       this.force
            .links(links);

       this.force.linkDistance(30);

        this.linkJoin = this.svg.select("#links").selectAll('.link')
           .data(this.force.links());

        this.linkJoin
           .enter().append('line')
           .attr('class', 'link');

       this.linkJoin
            .exit().remove();

        this.circleJoin = this.svg.select("#nodes").selectAll("circle")
                .data(this.force.nodes(), 
                      function(d) { 
                        return d.name; }
                      );

        this.circleJoin.enter().append("circle")
                .attr("r", 10)
                .style("fill",
                    function(d) {
                        return ((d.ap) ? "#FF3D00": "#FFBB00")
                    })
                .call(this.force.drag());

        this.circleJoin.exit().remove();

        this.force.on('tick', function() {
            this.linkJoin
                .attr('x1', function(d) { return d.source.x; })
                .attr('y1', function(d) { return d.source.y; })
                .attr('x2', function(d) { return d.target.x; })
                .attr('y2', function(d) { return d.target.y; });
            this.circleJoin
                .attr('cx', function(d) { return d.x; })
                .attr('cy', function(d) { return d.y; });
        }.bind(this));

        this.force.alpha(0.1);
        this.force.start();
   }
});

React.render(
  <LiteralJSON url="api/all_radios" poll={2000}/>,
  document.getElementById('content')
);


