<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2>D3 Box Plot</h2>
      <p>Source: https://www.d3-graph-gallery.com/graph/boxplot_basic.html</p>
    </div>
    <div id="boxplot"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'D3BoxPlot',
  data() {
    return {
      sampleData: [12, 19, 11, 13, 12, 22, 13, 4, 15, 16, 18, 19, 20, 12, 11, 9],
    };
  },
  mounted() {
    this.generateBoxPlot();
  },
  methods: {
    generateBoxPlot() {
      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

      // append the svg object to the body of the page
      var svg = d3
        .select('#boxplot')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      // Compute summary statistics used for the box:
      var data_sorted = this.sampleData.sort(d3.ascending);
      var q1 = d3.quantile(data_sorted, 0.25);
      var median = d3.quantile(data_sorted, 0.5);
      var q3 = d3.quantile(data_sorted, 0.75);
      var interQuantileRange = q3 - q1;
      var min = q1 - 1.5 * interQuantileRange;
      var max = q1 + 1.5 * interQuantileRange;

      // Show the Y scale
      var y = d3
        .scaleLinear()
        .domain([0, 24])
        .range([height, 0]);
      svg.call(d3.axisLeft(y));

      // a few features for the box
      var center = 200;
      var width = 100;

      // Show the main vertical line
      svg
        .append('line')
        .attr('x1', center)
        .attr('x2', center)
        .attr('y1', y(min))
        .attr('y2', y(max))
        .attr('stroke', 'black');

      // Show the box
      svg
        .append('rect')
        .attr('x', center - width / 2)
        .attr('y', y(q3))
        .attr('height', y(q1) - y(q3))
        .attr('width', width)
        .attr('stroke', 'black')
        .style('fill', '#69b3a2');

      // show median, min and max horizontal lines
      svg
        .selectAll('toto')
        .data([min, median, max])
        .enter()
        .append('line')
        .attr('x1', center - width / 2)
        .attr('x2', center + width / 2)
        .attr('y1', function(d) {
          return y(d);
        })
        .attr('y2', function(d) {
          return y(d);
        })
        .attr('stroke', 'black');
    },
  },
};
</script>
