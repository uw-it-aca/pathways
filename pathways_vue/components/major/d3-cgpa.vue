// d3-cgpa.vue

<template>
  <div class="card mb-5">
    <div class="card-body" v-if="!showCard">
      <h3>Declared major cumulative GPA distribution</h3>
      <div class="alert alert-info" role="alert">
      <p>No major GPA information for {{this.majorData.major_title}} was found. Here are some possible reasons:</p>
        <ul>
          <li>The major is new and doesn’t have enough student data to generate plots</li>
          <li>This major is no longer offered </li>
        </ul>
      </div>
      </div>
    <div v-else class="card-body">
      <h3>Declared major cumulative GPA distribution</h3>
      <div class="px-1 py-1">
        <p>Every student’s cumulative GPA at time of major declaration over the last {{ yearCount }} years.
            <a
            tabindex="0"
            class="info-gpa"
            role="button"
            data-bs-toggle="popover"
            data-bs-trigger="focus"
            title="Cumulative GPA Distribution"
            data-bs-content="This histogram represents data in a range of buckets along the horizontal line, or x-axis. The vertical line, or y-axis, represents the number of outcomes for each bucket."
          >
            <i class="bi bi-info-circle-fill"></i>
          </a>
        </p>
        <p class="fst-italic">
          <small>
            <i class="bi bi-exclamation-circle me-1"></i>Remember that GPA is just one of many factors that goes into major admissions decisions.
          </small>
        </p>
      </div>
      <ul class="nav nav-pills">
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: gpa_2yr_active }"
            aria-current="page"
            href="#"
            @click.prevent="selectChart('2yr')"
          >Last 2 Years</a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: !gpa_2yr_active }"
            href="#"
            @click.prevent="selectChart('5yr')"
          >Last 5 Years</a>
        </li>
      </ul>
      <p v-if="yearCount === 2 && !show2Year">
        {{ majorData.credential_title }} did not have enough students in the last 2 years to generate a GPA graph.
      </p>
      <p v-else-if="yearCount === 5 && !show5Year">
        {{ majorData.credential_title }} did not have enough students in the last 5 years to generate a GPA graph.
      </p>
      <div v-show="showGraph">
        <div id="histogram" class="mt-2"></div>
        <small>
          Number
          of students in this sample: {{ total_count }}
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { Popover } from 'bootstrap';
import numeral from 'numeral';

export default {
  name: 'D3Cgpa',
  data() {
    return {
      gpa_2yr_active: true,
      total_count: 0
    };
  },
  props: {
    majorData: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    if(this.showCard){
      var popover = new Popover(document.querySelector('.info-gpa'));
    }

    this.generateChart(this.majorData.gpa_2yr);
  },
  watch: {
    majorData: function () {
      this.generateChart(this.majorData.gpa_2yr);
    }
  },
  computed: {
    showCard(){
      return this.majorData.gpa_2yr.length > 0 || this.majorData.gpa_5yr.length > 0
    },
    yearCount() {
      if (this.gpa_2yr_active) {
        return 2;
      } else {
        return 5;
      }
    },
    formatGPA() {
      if (d.gpa == '50') {
        var newFormat = d3.format("");
      } else {
        var newFormat = d3.format(".2n");
      }
    },
    show2Year(){
      let count = 0
      for (const value of this.majorData.gpa_2yr){
        count += value.count
      }
      return count > 0;
    },
    show5Year(){
      let count = 0
      for (const value of this.majorData.gpa_5yr){
        count += value.count
      }
      return count > 0;
    },
    showGraph(){
      if(this.yearCount === 2){
        return this.show2Year;
      } else if(this.yearCount === 5){
        return this.show5Year;
      }
    }
  },
  methods: {
    selectChart(year) {
      if (year === '2yr') {
        this.gpa_2yr_active = true;
        this.generateChart(this.majorData.gpa_2yr);
      } else if (year === '5yr') {
        this.gpa_2yr_active = false;
        this.generateChart(this.majorData.gpa_5yr);
      }

    },
    generateChart(gpa_data) {
      if((this.yearCount === 2 && !this.show2Year)
        || (this.yearCount === 5 && !this.show5Year)){
        return;
      }
      if (this.showCard) {
        // clear chart
        document.getElementById("histogram").innerHTML = "";

        // Update count
        var count = gpa_data.reduce(function (accumulator, currentValue) {
          return accumulator + currentValue.count;
        }, 0);
        this.total_count = numeral(count).format('0,0');

        // set the dimensions and margins of the graph
        var margin = {top: 10, right: 30, bottom: 50, left: 50},
          width = 800 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom,
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
          .select('#histogram')
          .append('svg')
          //.attr("width", width + margin.left + margin.right)
          //.attr("height", height + margin.top + margin.bottom)
          .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Scale the range of the data in the domains
        x.domain(gpa_data.map(function (d) {
          return d.gpa / 10;
        }));
        y.domain([0, d3.max(gpa_data, function (d) {
          return d.count;
        })]);

        // append the rectangles for the bar chart
        svg.selectAll(".bar")
          .data(gpa_data)
          .enter().append("rect")
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
            tooltip.transition()
              .style("opacity", 1);
            tooltip.html(`GPA: ${d.gpa / 10} Total ${d.count}`)
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
          .style("font-size", "0.85rem")
          .classed("chart-label", true)
          .text("Number of students");

        svg.append("text")
          .attr('x', width / 2)
          .attr('y', height + margin.bottom)
          .style("text-anchor", "middle")
          .style("font-size", "0.85rem")
          .text("GPA");

        // add the x Axis
        svg.append("g")
          .attr('class', 'x axis')
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickValues(x.domain().filter(function (d, i) {
            return !(i % 5)
          })).tickFormat(this.newFormat));

        // add the y Axis
        svg.append("g")
          .call(d3.axisLeft(y));
      }
    }
  },
};
</script>

<style lang="scss">
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
  padding: 4px;
  background: #000;
  color: #fff;
  border-radius: 4px;
  width: 4rem;
  height: 2.5rem;
  font: 12px sans-serif;
  pointer-events: none;
}
</style>
