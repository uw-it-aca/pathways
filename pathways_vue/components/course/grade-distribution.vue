// grade-distribuition.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">
        Course Grade Distribution
      </h2>
      <p aria-hidden="true">
        This graph represents the distribution of grades for every student who
        completed
        <strong>{{ course.course_id }}</strong> over the past 5 years.
        <a
          tabindex="0"
          class="info-gcd"
          role="button"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          title="Course Grade Distribution"
          data-bs-content="This histogram represents data in a range of buckets along the horizontal line, or x-axis. The vertical line, or y-axis, represents the number of outcomes for each bucket."
        >
          <i class="bi bi-info-circle-fill me-0"></i>
        </a>
      </p>
      <div v-if="total_count < 8">
        <div class="alert alert-purple" role="alert">
          <p>
            Course grade distribution is not available for
            <strong>{{ course.course_id }}</strong> because there isn’t enough
            final grade data to generate plots.
          </p>
        </div>
      </div>
      <div v-else class="p-3">
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            v-model="viewDataTable"
            id="ToggleDataTable"
          />
          <label class="form-check-label" for="ToggleDataTable"
            >Display data as a table</label
          >
        </div>
      </div>
      <div
        aria-hidden="true"
        id="gcd-graph"
        :class="[viewDataTable ? 'visually-hidden' : '']"
      />

      <div v-if="total_count > 8" id="dataTable">
        <table class="table" v-if="viewDataTable">
          <caption class="caption-top">
            Number of grades in this sample:
            {{
              total_count
            }}
            (5 years). Data does not include pass/fail grades.
          </caption>
          <thead>
            <tr>
              <th scope="col">Course Grade</th>
              <th scope="col">Number of Students</th>
              <th scope="col">Percentage of Students</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="value in zeroCount" v-bind:key="value.count">
              <td>{{ value.gpa / 10 }}</td>
              <td>{{ value.count }}</td>
              <td>{{ distributionPercentage(value.count) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p :class="[viewDataTable ? 'visually-hidden' : '']">
        <small
          >Number of grades in this sample:
          <strong>{{ total_count }}</strong> (5 years).<br />
          The graph does not include pass/fail grades.
        </small>
      </p>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { Popover } from "bootstrap";
//import numeral from "numeral";

export default {
  name: "GradeDistribution",
  data() {
    return {
      total_count: 0,
      viewDataTable: false,
    };
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    var popover = new Popover(document.querySelector(".info-gcd"));
    this.generateChart(this.course.gpa_distro);
  },
  watch: {
    course: function (course) {
      this.generateChart(course.gpa_distro);
    },
  },
  computed: {
    formatGPA() {
      var newFormat = "";
      if (this.gpa == "50") {
        newFormat = d3.format("");
      } else {
        newFormat = d3.format(".2n");
      }
      return newFormat;
    },
    zeroCount: function () {
      return this.course.gpa_distro.filter(function (value) {
        return value.count > 0;
      });
    },
  },
  methods: {
    distributionPercentage(count) {
      return ((count / this.total_count) * 100).toFixed(2);
    },
    generateChart(gpa_data) {
      let vue = this;

      // clear chart
      document.getElementById("gcd-graph").innerHTML = "";

      // Update count
      var count = gpa_data.reduce(function (accumulator, currentValue) {
        return accumulator + currentValue.count;
      }, 0);
      this.total_count = count;

      const s_count = this.total_count;

      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 50, left: 50 },
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom,
        rwidth = width + margin.left + margin.right,
        rheight = height + margin.top + margin.bottom;

      var tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
        .style("left", "-9999px");

      // set the ranges
      var x = d3.scaleBand().range([0, width]).padding(0.3);
      var y = d3.scaleLinear().range([height, 0]);
      // append the svg object to the body of the page
      // append a 'group' element to 'svg'
      // moves the 'group' element to the top left margin
      var svg = d3
        .select("#gcd-graph")
        .append("svg")
        .attr("class", function () {
          if (s_count < 8) {
            return "d-none";
          } else {
            return "display";
          }
        })
        .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Scale the range of the data in the domains
      x.domain(
        gpa_data.map(function (d) {
          return d.gpa / 10;
        })
      );
      y.domain([
        0,
        d3.max(gpa_data, function (d) {
          return d.count;
        }),
      ]);
      // append the rectangles for the bar chart
      svg
        .selectAll(".bar")
        .data(gpa_data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
          return x(d.gpa / 10);
        })
        .attr("width", x.bandwidth())
        .attr("y", function (d) {
          return y(d.count);
        })
        .attr("height", function (d) {
          return height - y(d.count);
        })
        .on("mouseover", function (event, d) {
          tooltip.transition().style("opacity", 1);
          tooltip
            .html(
              `Grade ${d.gpa / 10}<br/>
              ${vue.distributionPercentage(d.count)}% (${d.count} total)`
            )
            .style("left", event.pageX + "px")
            .style("top", event.pageY - 28 + "px");
        })
        .on("mouseout", function () {
          tooltip.transition().style("opacity", 0);
        });

      svg
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 5 - margin.left)
        .attr("x", 0 - height / 2)
        .attr("dy", "0.5em")
        .style("text-anchor", "middle")
        .style("font-size", "0.85rem")
        .classed("chart-label", true)
        .text("Number of Students");

      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", height + margin.bottom)
        .style("text-anchor", "middle")
        .style("font-size", "0.85rem")
        .text("Course Grade");

      // add the x Axis
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(
          d3
            .axisBottom(x)
            .tickValues(
              x.domain().filter(function (d, i) {
                return !(i % 5);
              })
            )
            .tickFormat(this.newFormat)
        );

      // add the y Axis
      svg.append("g").call(d3.axisLeft(y));
    },
  },
};
</script>

<style lang="scss">
.chart-label {
  color: red;
}

#gcd-graph {
  margin-bottom: 1rem;
}

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
  shape-rendering: crispedges;
}

div.tooltip {
  position: absolute;
  text-align: left;
  white-space: nowrap;
  line-height: 1;
  padding: 3px;
  background: #000;
  color: #fff;
  border-radius: 4px;
  width: 7.5rem;
  height: 2.5rem;
  font-size: 12px sans-serif;
  pointer-events: none;
}
</style>
