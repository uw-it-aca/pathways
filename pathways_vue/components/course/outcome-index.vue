// outcome-index.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Outcome Index (COI)</h3>
      <p>
        Using prior course data, this index compares estimated fail/withdrawal rates against actual
        fail/withdrawal rates.
        <a
          tabindex="0"
          class="info-popper"
          role="button"
          data-bs-toggle="popover"
          data-bs-trigger="focus"
          title="Course Outcome Indicator"
          data-bs-content="A lower number (0-2) indicates that fewer people completed the course than expected. A middle number (2-3) indicates the course is on target with expectations. A higher (3-5) number indicates that more people completed the course than anticipated."
        >
          <i class="bi bi-info-circle-fill"></i>
        </a>
      </p>
      <div id="coiGraph" />
      <div class="coi-key">
        <p class="fw-bold">Key</p>

        <dl class="row">
          <dt class="col-sm-6">
            <i style="color: #ff8c00" class="bi bi-triangle-fill"></i>
            <span class="key-desc">{{course_id}}</span>
          </dt>
          <dd v-if="course_coi" class="col-sm-6 key-coi">COI: <strong>{{course_coi}}</strong></dd>
          <dd v-else class="col-sm-6 key-coi">No Data</dd>
          <dt class="col-sm-6">
            <i class="bi bi-circle-fill"></i>
            <span class="key-desc">Average course in {{curric_abbr}} curriculum</span>
          </dt>
          <dd v-if="curric_coi" class="col-sm-6 key-coi">COI: <strong>{{curric_coi}}</strong></dd>
          <dd v-else class="col-sm-6 key-coi">No Data</dd>
          <dt class="col-sm-6">
            <i class="bi bi-square-fill"></i>
            <span class="key-desc">Average {{course_level}} Level Course at UW</span>
          </dt>
          <dd v-if="course_level_coi" class="col-sm-6 key-coi">COI: <strong>{{course_level_coi}}</strong></dd>
          <dd v-else class="col-sm-6 key-coi">No Data</dd>
        </dl>
        <p>*<!--{{percent_in_range}}--> <small>54% of all UW courses fall within the <!--{{range_text}}-->2 - 3 range.<br>
          <strong>No Data</strong> means there is not enough data to generate a COI plot.</small>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { Popover } from 'bootstrap';

export default {
  name: 'OutcomeScore',
  data() {
    return {
      percent_in_range: null,
      course_coi: null,
      course_level_coi: null,
      curric_coi: null,
      curric_id: null,
      curric_abbr: null,
      course_num: null
    };
  },
    props: {
    course: {
      type: Object,
      required: true,
    },
  },
  watch: {
    course: function (course){
      this.percent_in_range = course.coi_data.percent_in_range;
      this.course_coi = course.coi_data.course_coi;
      this.course_level_coi = course.coi_data.course_level_coi;
      this.curric_coi = course.coi_data.curric_coi;
      this.course_id = course.course_id;

      var split_pos = this.course_id.lastIndexOf(" ");
      this.curric_abbr = this.course_id.substring(0, split_pos);
      this.course_num = parseInt(this.course_id.substring(split_pos + 1,
        this.course_id.length));
      this.generateRect();
    }
  },
  mounted() {
    var popover = new Popover(document.querySelector('.info-popper'));
  },
  computed: {
    course_level: function (){
      return Math.floor(this.course_num/100)*100;
    },
    range_text: function (){
      if(this.course_coi <= 1){
        return "0 - 1"
      } else if(this.course_coi <= 2){
        return "1 - 2"
      } else if(this.course_coi <= 3){
        return "2 - 3"
      }else if(this.course_coi <= 4){
        return "3 - 4"
      }else if(this.course_coi <= 5){
        return "4 - 5"
      }
    }
  },
  methods: {
    generateRect() {
      // Clear any previous graphs
      document.getElementById("coiGraph").innerHTML = "";
      const margin = { top: 20, right: 10, bottom: 20, left: 10 };
      const width = 600 - margin.left - margin.right,
        height = 100 - margin.top - margin.bottom,
        rwidth = width + margin.left + margin.right,
        rheight = height + margin.top + margin.bottom;

      // Create the 5.0 COI scale
      const x = d3
        .scaleLinear()
        .domain([0, 5]) // This is what is written on the Axis: from 0 to 100
        .range([0, width]); // This is where the axis is placed: from 0px to 600px

      // Append SVG to container
      const svg = d3
        .select('#coiGraph')
        .append('svg')
        .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
        .append("g")
        .attr("transform","translate(" + margin.left + "," + margin.top + ")");

      // Draw the rect that expands width, light blue
      svg
        .append('rect')
        .attr('x', 0)
        .attr('y', 52)
        .attr('width', width)
        .attr('height', 7)
        .attr('fill-opacity', '0.6')
        .attr('fill', '#A2D3FF');

      // Draw the middle rect, dark blue
      svg
        .append('rect')
        .attr('x', 232)
        .attr('y', 52)
        .attr('width', 116)
        .attr('height', 7)
        .attr('fill-opacity', '0.6')
        .attr('fill', '#055CAA');

      // Pull in data to plot on line
      const CourseCOI = this.course_coi;
      const CurrCOI = this.curric_coi;
      const UwCOI = this.course_level_coi;

      // Draw the axis
      let xAxisGenerator = d3.axisBottom(x).ticks(5).tickSize(-20);
      let xAxis = svg.append('g');

      xAxis
        .attr('transform', 'translate(0,65)') // This controls the vertical position of the Axis
        .call(xAxisGenerator)
        .select('.domain')
        .remove();

      const g = svg.append('g');

      g.append('path') // creates a triangle symbol for course COI and plots on x axis
        .attr('d', d3.symbol().type(d3.symbolTriangle).size(180))
        .attr('class', function(d) {
            if (CourseCOI == null) { return "d-none" }
            else { return "display" }
            ;})
        .attr('transform', 'translate(' + x(CourseCOI) + ', 55)')
        .style('fill', '#FF8C00');

      g.append('path') // creates a square symbol for all uw COI and plots on x axis
        .attr('d', d3.symbol().type(d3.symbolSquare).size(180))
        .attr('class', function(d) {
            if (UwCOI == null) { return "d-none" }
            else { return "display" }
            ;})
        .attr('transform', 'translate(' + x(UwCOI) + ', 55)');

      g.append('path') // creates a circle symbol for curriculum COI and plots on x axis
        .attr('d', d3.symbol().type(d3.symbolCircle).size(180))
        .attr('class', function(d) {
            if (CurrCOI == null) { return "d-none" }
            else { return "display" }
            ;})
        .attr('transform', 'translate(' + x(CurrCOI) + ', 55)');

      g.append('text')
        .attr('x', -2)
        .attr('y', 25)
        .attr('text-anchor', 'left')
        .style('font-size', '11px')
        .text('less completions than expected');

      g.append('text')
        .attr('x', 290)
        .attr('y', 25)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .text('on target with expectations*');

      g.append('text')
        .attr('x', 410)
        .attr('y', 25)
        .attr('text-anchor', 'right')
        .style('font-size', '11px')
        .text('more completions than expected');
    },
  },
};
</script>

<style lang="scss">
svg {
  padding-left: 10px;
}

.coi-key {
  font-size: 0.875rem;
}

.tick {
  stroke-width: 1.5;
}

.bi {
  margin-right: 1rem;
}
.key-desc {
  font-weight: normal;
}
.display-none {
  display: none;
}
</style>
