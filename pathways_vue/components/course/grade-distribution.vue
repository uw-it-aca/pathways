// grade-distribuition.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Grade Distribution</h3>
      <p aria-hidden="true">
        This graph represents the distribution of grades for every student who completed <strong>{{course.course_id}}</strong> over the past 5 years.
        <a
          tabindex="0"
          class="info-gcd"
          role="button"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          title="Course Grade Distribution"
          data-bs-content="This histogram represents data in a range of buckets along the horizontal line, or x-axis. The vertical line, or y-axis, represents the number of outcomes for each bucket."
        >
          <i class="bi bi-info-circle-fill"></i>
        </a>
      </p>
      <div aria-hidden="true" id="gcd_graph" />
      <div v-if="total_count < 8">
        <div class="alert alert-purple" role="alert">
          <p>Course grade distribution is not available for <strong>{{course.course_id}}</strong> because there isn’t enough final grade data to generate plots.</p>
        </div>
      </div>
      <div v-if="total_count > 8" id="dataTable" class="visually-hidden">
          <table class="table">
            <caption>This data table represents the distribution of grades for every student who completed <strong>{{course.course_id}}</strong> over the past 5 years.</caption>
            <thead>
              <tr>
                <th scope="col">Number of Students</th>
                <th scope="col">GPA</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="value in zeroCount" v-bind:key="value.count">
                <td>{{value.count}}</td>
                <td>{{value.gpa/10}}</td>
              </tr>
            </tbody>
          </table>
        </div>
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
    this.generateChart(this.course.gpa_distro);
  },
  watch:{
    course: function (course){
      this.generateChart(course.gpa_distro);
    }
  },
  computed: {
    formatGPA() {
      if (d.gpa == '50') {
        var newFormat = d3.format("");
      } else {
        var newFormat = d3.format(".2n");
      }
    },
    zeroCount: function() {
      return this.course.gpa_distro.filter(function(value) {
        return value.count > 0;
      })
    },
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

      const s_count = this.total_count; 

      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 30, left: 50 },
        width = 460 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom,
        rwidth = width + margin.left + margin.right,
        rheight = height + margin.top + margin.bottom;

      var tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);

      // set the ranges
      var x = d3.scaleBand()
        .range([0, width])
        .padding(0.3);
      var y = d3.scaleLinear()
        .range([height, 0]);
      // append the svg object to the body of the page
      // append a 'group' element to 'svg'
      // moves the 'group' element to the top left margin
      var svg = d3
         .select('#gcd_graph')
        .append('svg')
        .attr('class', function(d) {
            if (s_count < 8) { return 'd-none' }
            else { return "display" }
            ;})
        .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
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
        .on("mouseover", function (event, d) {
          tooltip.transition()
            .style("opacity", 1);
          tooltip.html(`Grade ${d.gpa / 10} Total ${d.count}`)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function (d) {
          tooltip.transition()
            .style("opacity", 0);
        });

      svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 5 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "0.5em")
        .style("text-anchor", "middle")
        .style("font-size", "0.75rem")
        .classed("chart-label", true)
        .text("Number of Students");

      svg.append("text")
        .attr('x', width / 2)
        .attr('y', height + margin.bottom)
        .style("text-anchor", "middle")
        .style("font-size", "0.75rem")
        .text("Course Grade");

      // add the x Axis
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues(x.domain().filter(function (d, i) { return !(i % 5) })).tickFormat(this.newFormat));

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

.bar {
  fill: #4b2e83;
}
.bar:hover {
  fill: #333;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

div.tooltip {
  position: absolute;
  text-align: center;
  line-height: 1;
  padding: 3px;
  background: #000;
  color: #fff;
  border-radius: 4px;
  width: 5rem;
  height: 3.5rem;
  font: 12px sans-serif;
  pointer-events: none;
}

</style>
