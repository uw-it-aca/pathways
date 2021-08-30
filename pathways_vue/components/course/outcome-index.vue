// outcome-index.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Outcome Index (COI)</h3>
      <p>
        Using prior course data, this index compares estimated fail/withdrawal rates against actual
        fail/withdrawal rates. <a href="#"><i class="bi bi-info-circle-fill"></i></a>
      </p>
      <div id="coiGraph" />
      <div class="coi-key">
        <p class="fw-bold">Key</p>
        <p><i class="bi bi-triangle-fill"></i> CHEM 162</p>
        <p><i class="bi bi-circle-fill"></i> Average course in CHEM curriculum</p>
        <p><i class="bi bi-square-fill"></i> Average 100 Level Course at UW</p>
        <p>*53.9% of all UW courses fall within the 2-3 range</p>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'OutcomeScore',
  data() {
    return {
      coi: [
        { outcome: 'course', value: 2.7 },
        { outcome: 'curr', value: 2.0 },
        { outcome: 'uw', value: 1.8 },
      ],
    };
  },
  mounted() {
    this.generateRect();
  },
  methods: {
    generateRect() {
      const margin = { top: 20, right: 10, bottom: 20, left: 10 };
      const width = 600 - margin.left - margin.right,
        height = 100 - margin.top - margin.bottom;

      // Create the 5.0 COI scale
      const x = d3
        .scaleLinear()
        .domain([0, 5]) // This is what is written on the Axis: from 0 to 100
        .range([0, width]); // This is where the axis is placed: from 0px to 600px

      // Append SVG to container
      const svg = d3
        .select('#coiGraph')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

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

      const CourseCOI = this.coi.filter(function (d) {
        return d.outcome === 'course';
      })[0].value;

      const CurrCOI = this.coi.filter(function (d) {
        return d.outcome === 'curr';
      })[0].value;

      const UwCOI = this.coi.filter(function (d) {
        return d.outcome === 'uw';
      })[0].value;

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
        .attr('transform', 'translate(' + x(CourseCOI) + ', 51) rotate(180)')
        .style('fill', '#FF8C00');

      g.append('path') // creates a square symbol for all uw COI and plots on x axis
        .attr('d', d3.symbol().type(d3.symbolSquare).size(180))
        .attr('transform', 'translate(' + x(UwCOI) + ', 55)');

      g.append('path') // creates a circle symbol for curriculum COI and plots on x axis
        .attr('d', d3.symbol().type(d3.symbolCircle).size(180))
        .attr('transform', 'translate(' + x(CurrCOI) + ', 55)');

      /*g.selectAll('path')
        .data(sortedCOI)
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => color(i))
        .attr('stroke', '#FFF')
        .attr('stroke-width', '1px')
        .on('mouseenter', function () {
          d3.select(this).transition().duration(200).attr('opacity', 0.5);
        })
        .on('mouseout', function () {
          d3.select(this).transition().duration(200).attr('opacity', 1);
        });*/

      g.selectAll('text')
        //.data(this.coi)
        .enter()
        .append('text')
        .text((d) => `${d.outcome}  COI ${d.value}`)
        .classed('legend-text', true)
        .attr('x', -150)
        .attr('dy', -8)
        .attr('y', (d, i) => -(i + 1) * 25);

      //g.attr('transform', 'translate(150,235)');
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

.bi-triangle-fill {transform: rotate(20deg);}
</style>
