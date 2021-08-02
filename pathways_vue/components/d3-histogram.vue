// d3-histogram.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Declared major cumulative GPA distribution</h3>
      <div class="alert alert-secondary" role="alert">
        <p>Remember that GPA is just one of many factors that goes into admissions decisions.</p>
      </div>
      <ul class="nav nav-pills">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Last 2 Years</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Last 5 Years</a>
        </li>
      </ul>

      <div id="histogram" class="m-3"></div>
      <small
        >Every student’s cumulative GPA at time of major declaration over the last 5 years. Number
        of students in this sample: 467</small
      >
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'D3Histogram',
  data() {
    return {
      sampledata: [
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 2.52, 3.52, 3.52, 2.52, 3.52, 3.52, 2.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52, 3.52,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58, 3.58,
        3.74, 3.74, 3.74, 2.74, 3.74, 3.74, 3.74, 3.74, 2.74, 3.74, 3.74, 2.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74, 3.74,
        3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55,
        3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55,
        3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55, 3.55,
      ],
    };
  },
  mounted() {
    this.generateHistogram();
  },
  methods: {
    generateHistogram() {
      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

      // append the svg object to the body of the page
      var svg = d3
        .select('#histogram')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      // X axis: scale and draw:
      var x = d3
        .scaleLinear()
        .domain([0, 4.0]) // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
        .range([0, width]);
      svg
        .append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x));

      // set the parameters for the histogram
      var histogram = d3
        .histogram()
        .value(function (d) {
          return d;
        }) // I need to give the vector of value
        .domain(x.domain()) // then the domain of the graphic
        .thresholds(x.ticks(70)); // then the numbers of bins

      // And apply this function to data to get the bins
      var bins = histogram(this.sampledata);

      // Y axis: scale and draw:
      var y = d3.scaleLinear().range([height, 0]);
      y.domain([
        0,
        d3.max(bins, function (d) {
          return d.length;
        }),
      ]); // d3.hist has to be called before the Y axis obviously
      svg.append('g').call(d3.axisLeft(y));

      // append the bar rectangles to the svg element
      svg
        .selectAll('rect')
        .data(bins)
        .enter()
        .append('rect')
        .attr('x', 1)
        .attr('transform', function (d) {
          return 'translate(' + x(d.x0) + ',' + y(d.length) + ')';
        })
        .attr('width', function (d) {
          return x(d.x1) - x(d.x0) - 1;
        })
        .attr('height', function (d) {
          return height - y(d.length);
        })
        .style('fill', '#69b3a2');
    },
  },
};
</script>

<style lang="scss"></style>