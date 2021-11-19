// grade-distribuition.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Grade Distribution</h3>
      <p>
        This graph represents the distribution of grades for every student who completed <strong>{{course.course_id}}</strong> over the past 5 years.
        <a
          tabindex="0"
          class="info-gcd"
          role="button"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          title="Course Grade Distribution"
          data-bs-content="What is CGD?"
        >
          <i class="bi bi-info-circle-fill"></i>
        </a>
      </p>
      <div id="gcd_graph" />
      <p><small>Number of grades in this sample: {{total_count}} (5 years). Data not instructor-specific.</small></p>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { Popover } from 'bootstrap';
import numeral from 'numeral';

export default {
  name: "GradeDistribution",
  data() {
    return {
      total_count: 0
    };
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  mounted() {

    var popover = new Popover(document.querySelector('.info-gcd'));
  },
  watch:{
    course: function (course){
      this.generateChart(course.gpa_distro);
    }
  },
  methods: {
    generateChart(gpa_data){
      // clear chart
      document.getElementById("gcd_graph").innerHTML = "";

      // Update count
      var count = gpa_data.reduce(function(accumulator, currentValue) {
          return accumulator + currentValue.count;
        }, 0);
      this.total_count = numeral(count).format('0,0');

      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

      // set the ranges
      var x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);
      var y = d3.scaleLinear()
        .range([height, 0]);
      // append the svg object to the body of the page
      // append a 'group' element to 'svg'
      // moves the 'group' element to the top left margin
      var svg = d3
         .select('#gcd_graph')
        .append('svg')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform","translate(" + margin.left + "," + margin.top + ")");

      // Scale the range of the data in the domains
      x.domain(gpa_data.map(function(d) { return d.gpa/10; }));
      y.domain([0, d3.max(gpa_data, function(d) { return d.count; })]);
      // append the rectangles for the bar chart
      svg.selectAll(".bar")
        .data(gpa_data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.gpa/10); })
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d.count); })
        .attr("height", function(d) { return height - y(d.count); })
        .style('fill', '#69b3a2');
      // add the x Axis
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // add the y Axis
      svg.append("g")
        .call(d3.axisLeft(y));

    }
  },
};
</script>

<style lang="scss">
.chart-label {color: red;}
#gcd_graph {margin-bottom: 1rem;}

</style>
