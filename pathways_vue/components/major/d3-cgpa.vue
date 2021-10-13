// d3-cgpa.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Declared major cumulative GPA distribution</h3>
      <div class="px-1 py-1">
        <p>Every student’s cumulative GPA at time of major declaration over the last {{yearCount}} years.</p>
        <p class="fst-italic"><small><i class="bi bi-exclamation-circle me-1"></i>Remember that GPA is just one of many factors that goes into admissions decisions.</small></p>
      </div>
      <ul class="nav nav-pills">
        <li class="nav-item">
          <a class="nav-link"
             :class="{active:gpa_2yr_active}"
             aria-current="page"
             href="#"
             @click.prevent="selectChart('2yr')">Last 2 Years</a>
        </li>
        <li class="nav-item">
          <a class="nav-link"
             :class="{active:!gpa_2yr_active}"
             href="#"
             @click.prevent="selectChart('5yr')">Last 5 Years</a>
        </li>
      </ul>

      <div id="histogram" class="m-3"></div>
      <small>Number
        of students in this sample: {{total_count}}</small
      >
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
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
    // this.generateHistogram();
    this.generateChart(this.majorData.gpa_2yr);
  },
  watch: {
    majorData:  function(){
      this.generateChart(this.majorData.gpa_2yr);
    }
  },
  computed: {
    yearCount() {
      if(this.gpa_2yr_active){
        return 2;
      } else {
        return 5;
      }
    },
  },
  methods: {
    selectChart(year){
      if(year === '2yr'){
        this.generateChart(this.majorData.gpa_2yr);
        this.gpa_2yr_active = true;
      } else if(year === '5yr'){
        this.gpa_2yr_active = false;
        this.generateChart(this.majorData.gpa_5yr);
      }

    },
    generateChart(gpa_data){
      // clear chart
      document.getElementById("histogram").innerHTML = "";

      // Update count
      var count = gpa_data.reduce(function(accumulator, currentValue) {
          return accumulator + currentValue.count;
        }, 0);
      this.total_count = numeral(count).format('0,0');

      // set the dimensions and margins of the graph
      var margin = { top: 10, right: 30, bottom: 50, left: 40 },
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

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
        .style('fill', '#4b2e83');

        svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
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
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues(x.domain().filter(function(d,i) { return !(i % 5)})));

      // add the y Axis
      svg.append("g")
        .call(d3.axisLeft(y));
    }
  },
};
</script>

<style lang="scss"></style>
