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
        { outcome: 'CHEM 162', value: 8.5 },
        { outcome: 'All CHEM', value: 7.9 },
        { outcome: 'All UW', value: 6.9 },
      ],
    };
  },
  mounted() {
    this.generateRect();
  },
  methods: {
    generateRect() {
      const w = 600;
      const h = 200;

      const svg = d3.select('#coiGraph').append('svg').attr('width', w).attr('height', h);

      svg
        .append('rect')
        .attr('x', 10)
        .attr('y', 60)
        .attr('width', 580)
        .attr('height', 40)
        //.attr('stroke', 'black')
        .attr('fill', '#69a3b2');

      // Create the scale
      const x = d3
        .scaleLinear()
        .domain([0, 5.0]) // This is what is written on the Axis: from 0 to 100
        .range([0, 580]); // This is where the axis is placed: from 100px to 800px

      // Draw the axis
      svg
        .append('g')
        .attr('transform', 'translate(10,100)') // This controls the vertical position of the Axis
        .call(d3.axisBottom(x).tickValues([0, 5]));

      /*const sortedCOI = this.coi.sort((a, b) => (a.value > b.value ? 1 : -1));
      const color = d3
        .scaleSequential()
        .interpolator(d3.interpolateRgb('purple', 'blue'))
        .domain([0, 3]);

      const max_coi = d3.max(sortedCOI, (o) => o.value);

      const angleScale = d3
        .scaleLinear()
        .domain([0, max_coi])
        .range([0, 1.5 * Math.PI]);

      const arc = d3
        .arc()
        .innerRadius((d, i) => (i + 1) * 25)
        .outerRadius((d, i) => (i + 2) * 25)
        .startAngle(angleScale(0))
        .endAngle((d) => angleScale(d.value));

      const g = svg.append('g');

      g.selectAll('path')
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
        });

      g.selectAll('text')
        .data(this.coi)
        .enter()
        .append('text')
        .text((d) => `${d.outcome} -  ${d.value} COI`)
        .attr('x', -150)
        .attr('dy', -8)
        .attr('y', (d, i) => -(i + 1) * 25);

      g.attr('transform', 'translate(300,155)');*/
    },
  },
};
</script>

<style lang="scss"></style>
