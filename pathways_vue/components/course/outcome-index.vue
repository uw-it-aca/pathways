// outcome-index.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Course Outcome Index (COI)</h3>
      <p>
        Using prior course data, this index compares estimated fail/withdrawal rates against actual
        fail/withdrawal rates.
      </p>
      <div id="arc" />
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'OutcomeIndex',
  data() {
    return {
      gdp: [
        { coi: 'CHEM 162', value: 8.5 },
        { coi: 'All CHEM', value: 7.9 },
        { coi: 'ALL UW', value: 6.9 },
        //{ country: 'Japan', value: 4.9 },
        //{ country: 'France', value: 2.8 },
      ],
    };
  },
  mounted() {
    this.generateArc();
  },
  methods: {
    generateArc() {
      const w = 500;
      const h = 300;

      const svg = d3
        .select('#arc')
        .append('svg')
        .attr('width', w)
        .attr('height', h);

      const sortedGDP = this.gdp.sort((a, b) => (a.value > b.value ? 1 : -1));
      const color = d3.scaleOrdinal(d3.schemeSet1);

      const max_gdp = d3.max(sortedGDP, o => o.value);

      const angleScale = d3
        .scaleLinear()
        .domain([0, max_gdp])
        .range([0, 1.5 * Math.PI]);

      const arc = d3
        .arc()
        .innerRadius((d, i) => (i + 1) * 25)
        .outerRadius((d, i) => (i + 2) * 25)
        .startAngle(angleScale(0))
        .endAngle(d => angleScale(d.value));

      const g = svg.append('g');

      g.selectAll('path')
        .data(sortedGDP)
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => color(i))
        .attr('stroke', '#FFF')
        .attr('stroke-width', '1px')
        .on('mouseenter', function() {
          d3.select(this)
            .transition()
            .duration(200)
            .attr('opacity', 0.5);
        })
        .on('mouseout', function() {
          d3.select(this)
            .transition()
            .duration(200)
            .attr('opacity', 1);
        });

      g.selectAll('text')
        .data(this.gdp)
        .enter()
        .append('text')
        .text(d => `${d.coi} -  ${d.value} COI`)
        .attr('x', -150)
        .attr('dy', -8)
        .attr('y', (d, i) => -(i + 1) * 25);

      g.attr('transform', 'translate(300,155)');
    },
  },
};
</script>

<style lang="scss"></style>
