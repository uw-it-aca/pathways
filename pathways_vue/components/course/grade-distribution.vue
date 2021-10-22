// grade-distribuition.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Grade Distribution</h3>
      <p>
        This graph represents the distribution of grades for every student who completed <strong>CHEM 162</strong> over the past 5 years.
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
      <p><small>Number of grades in this sample: 6988 (5 years). Data not instructor-specific.</small></p>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { Popover } from 'bootstrap';

export default {
  name: "GradeDistribution",
  data() {
    return {
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
    // generateGCD() {
    //   // set the dimensions and margins of the graph
    //   const margin = { top: 10, right: 30, bottom: 45, left: 40 },
    //     width = 600 - margin.left - margin.right,
    //     height = 270 - margin.top - margin.bottom;
    //
    //   // append the svg object to the body of the page
    //   const svg = d3
    //     .select('#gcd_graph')
    //     .append('svg')
    //     .attr('width', width + margin.left + margin.right)
    //     .attr('height', height + margin.top + margin.bottom)
    //     .append('g')
    //     .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    //
    //   // X axis: scale and draw:
    //   const x = d3
    //     .scaleLinear()
    //     .domain([0, 4.0]) // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
    //     .range([0, width]);
    //   svg
    //     .append('g')
    //     .attr('transform', 'translate(0,' + height + ')')
    //     .call(d3.axisBottom(x));
    //
    //   // set the parameters for the histogram
    //   const histogram = d3
    //     .histogram()
    //     .value(function (d) {
    //       return d;
    //     }) // I need to give the vector of value
    //     .domain(x.domain()) // then the domain of the graphic
    //     .thresholds(x.ticks(70)); // then the numbers of bins
    //
    //   // And apply this function to data to get the bins
    //   const bins = histogram(this.sampledata);
    //
    //   // Y axis: scale and draw:
    //   const y = d3.scaleLinear().range([height, 0]);
    //   y.domain([
    //     0,
    //     d3.max(bins, function (d) {
    //       return d.length;
    //     }),
    //   ]); // d3.hist has to be called before the Y axis obviously
    //   svg.append('g').call(d3.axisLeft(y));
    //
    //   svg.append("text")
    //   .attr("transform", "rotate(-90)")
    //   .attr("y", 0 - margin.left)
    //   .attr("x",0 - (height / 2))
    //   .attr("dy", "0.5em")
    //   .style("text-anchor", "middle")
    //   .style("font-size", "0.85rem")
    //   .classed("chart-label", true)
    //   .text("Number of students");
    //
    //   svg.append("text")
    //   .attr('x', width / 2)
    //   .attr('y', height + margin.bottom)
    //   .style("text-anchor", "middle")
    //   .style("font-size", "0.85rem")
    //   .text("Course Grade");
    //
    //   // append the bar rectangles to the svg element
    //   svg
    //     .selectAll('rect')
    //     .data(bins)
    //     .enter()
    //     .append('rect')
    //     .attr('x', 1)
    //     .attr('transform', function (d) {
    //       return 'translate(' + x(d.x0) + ',' + y(d.length) + ')';
    //     })
    //     .attr('width', function (d) {
    //       return x(d.x1) - x(d.x0);
    //     })
    //     .attr('height', function (d) {
    //       return height - y(d.length);
    //     })
    //     .style('fill', '#69b3a2');
    // },
    generateChart(gpa_data){
      console.log(gpa_data)
      // clear chart
      document.getElementById("gcd_graph").innerHTML = "";
      console.log('generated')
      console.log(typeof gpa_data)

      // Update count
      var count = gpa_data.reduce(function(accumulator, currentValue) {
          return accumulator + currentValue.count;
        }, 0);
      this.total_count = numeral(count).format('0,0');
console.log('generated1')
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
console.log('generated2')
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
console.log('generated3')
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
console.log('generated4')
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
