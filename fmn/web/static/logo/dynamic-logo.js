var w = 600,
    h = 700;

// Destroy the old logo first
d3.select("#static-logo").remove();

d3.json("static/logo/graph.json", function(json) {


  var force = d3.layout.force()
      .nodes(json.nodes)
      .links(json.links)
      .size([w, h])
      .linkDistance(60)
      .charge(-600)
      .on("tick", tick)
      .start();

  var svg = d3.select("#logo-container").append("svg:svg")
      .attr("width", w)
      .attr("height", h);

  // Per-type markers, as they don't inherit styles.
  svg.append("svg:defs").selectAll("marker")
      .data(["input", "output"])
    .enter().append("svg:marker")
      .attr("id", String)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -1.5)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
    .append("svg:path")
      .attr("d", "M0,-5L10,0L0,5");

  var path = svg.append("svg:g").selectAll("path")
      .data(force.links())
    .enter().append("svg:path")
      .attr("class", function(d) { return "link " + d.type; })
      .attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

  var node = svg.append("svg:g").selectAll(".node")
      .data(force.nodes())
    .enter().append("g").attr("class", "node")
      .call(force.drag);

  node.append("image")
      .attr("class", function (d) { return "group-" + d.group })
      .attr("xlink:href", function (d) { return d.icon })
      .attr("x", -8)
      .attr("y", -8)
      .attr("width", 16)
      .attr("height", 16);

  var text = svg.append("svg:g").selectAll("g")
      .data(force.nodes())
    .enter().append("svg:g");

  // A copy of the text with a thick white stroke for legibility.
  text.append("svg:text")
      .attr("x", 8)
      .attr("y", ".31em")
      .attr("class", "shadow")
      .text(function(d) { return d.name; });

  text.append("svg:text")
      .attr("x", 8)
      .attr("y", ".31em")
      .text(function(d) { return d.name; });

  // Use elliptical arc path segments to doubly-encode directionality.
  function tick() {
    path.attr("d", function(d) {
      var dx = d.target.x - d.source.x,
          dy = d.target.y - d.source.y,
          dr = Math.sqrt(dx * dx + dy * dy);
      return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    });

    node.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });

    text.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  }
});
