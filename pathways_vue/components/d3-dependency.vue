<template>
  <div>
    <h2>D3 Dependency Graph Example</h2>
    <p>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Non dolor, cumque dolorum, commodi
      nemo ut ullam expedita cum ea soluta, similique a asperiores corrupti tenetur. Laborum
      incidunt dolorum tenetur magni.
    </p>
    <p>Source: https://bl.ocks.org/agnjunio/c83d7a4b9e787385885f6e21de0ec8e7</p>

    <div :style="{ width: width + 'px', height: height + 'px' }" class="dependency-test">
      <svg width="100%" height="100%"></svg>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'D3Dependency',
  data() {
    return {
      width: 1024,
      height: 768,
      selections: {},
      simulation: null,
      forceProperties: {
        center: {
          x: 0.5,
          y: 0.5,
        },
        charge: {
          enabled: true,
          strength: -300,
          distanceMin: 1,
          distanceMax: 2000,
        },
        collide: {
          enabled: true,
          strength: 0.7,
          iterations: 1,
          radius: 35,
        },
        forceX: {
          enabled: false,
          strength: 0.1,
          x: 0.5,
        },
        forceY: {
          enabled: false,
          strength: 0.35,
          y: 0.5,
        },
        link: {
          enabled: true,
          distance: 100,
          iterations: 1,
        },
      },
      data: {
        nodes: [],
        links: [],
      },
    };
  },
  computed: {
    nodes() {
      return this.data.nodes;
    },
    links() {
      return this.data.links;
    },
  },
  mounted() {
    this.simulation = d3
      .forceSimulation()
      .force('link', d3.forceLink())
      .force('charge', d3.forceManyBody())
      .force('collide', d3.forceCollide())
      .force('center', d3.forceCenter())
      .force('forceX', d3.forceX())
      .force('forceY', d3.forceY())
      .on('tick', this.tick);
    this.updateForces();

    this.selections.svg = d3.select(this.$el.querySelector('svg'));
    const svg = this.selections.svg;

    // Define the arrow marker
    svg
      .append('svg:defs')
      .selectAll('marker')
      .data(['end']) // Different link/path types can be defined here
      .enter()
      .append('svg:marker') // This section adds in the arrows
      .attr('id', String)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 43) // Prevents arrowhead from being covered by circle
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M0,-5L10,0L0,5');

    // Define arrow for self-links
    svg
      .append('svg:defs')
      .selectAll('marker')
      .data(['end-self'])
      .enter()
      .append('svg:marker') // This section adds in the arrows
      .attr('id', String)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 40)
      .attr('refY', -15)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 285)
      .append('svg:path')
      .attr('d', 'M0,-5L10,0L0,5');

    this.selections.graph = this.selections.svg.append('g');
    const graph = this.selections.graph;

    // You can set data in any ways you want...
    this.data = {
      nodes: [
        { name: 'firmware', group: 1, class: 'system' },
        { name: 'loader', group: 1, class: 'system' },
        { name: 'kernel', group: 1, class: 'system' },
        { name: 'systemd', group: 1, class: 'mount' },
        { name: '-.mount', group: 1, class: 'mount' },
        { name: 'init.scope', group: 1, class: 'init' },
        { name: 'system.slice', group: 1, class: 'init' },
        { name: 'system-getty.slice', group: 1, class: 'init' },
        { name: 'systemd-initctl.socker', group: 1, class: 'init' },
        { name: 'tmp.mount', group: 1, class: 'init' },
        { name: 'sys-devices', group: 2, class: 'init' },
        { name: 'boot.mount', group: 2, class: 'init' },
      ],
      links: [
        { source: 1, target: 0, value: 1, type: 'depends' },
        { source: 2, target: 1, value: 8, type: 'depends' },
        { source: 3, target: 2, value: 6, type: 'depends' },
        { source: 4, target: 3, value: 1, type: 'needs' },
        { source: 5, target: 3, value: 1, type: 'needs' },
        { source: 6, target: 3, value: 1, type: 'needs' },
        { source: 7, target: 3, value: 1, type: 'needs' },
        { source: 8, target: 3, value: 2, type: 'needs' },
        { source: 9, target: 3, value: 1, type: 'needs' },
        { source: 11, target: 10, value: 1, type: 'depends' },
        { source: 11, target: 3, value: 3, type: 'depends' },
        { source: 11, target: 2, value: 3, type: 'depends' },
        { source: 11, target: 3, value: 5, type: 'needs' },
      ],
    };
  },
  methods: {
    tick() {
      const transform = d => {
        return 'translate(' + d.x + ',' + d.y + ')';
      };

      const link = d => {
        return 'M' + d.source.x + ',' + d.source.y + ' L' + d.target.x + ',' + d.target.y;
      };

      const graph = this.selections.graph;
      graph.selectAll('path').attr('d', link);
      graph.selectAll('circle').attr('transform', transform);
      graph.selectAll('text').attr('transform', transform);
    },
    updateData() {
      this.simulation.nodes(this.nodes);
      this.simulation.force('link').links(this.links);

      const simulation = this.simulation;
      const graph = this.selections.graph;

      graph
        .selectAll('path')
        .data(simulation.force('link').links())
        .enter()
        .append('path')
        .attr('class', d => 'link ' + d.type)
        .exit()
        .remove();

      graph
        .selectAll('circle')
        .data(simulation.nodes())
        .enter()
        .append('circle')
        .attr('r', 30)
        .attr('class', d => d.class)
        .exit()
        .remove();

      graph
        .selectAll('text')
        .data(simulation.nodes())
        .enter()
        .append('text')
        .attr('x', 0)
        .attr('y', '.31em')
        .attr('text-anchor', 'middle')
        .text(d => d.name);

      // Add 'marker-end' attribute to each path
      const svg = d3.select(this.$el.querySelector('svg'));
      svg
        .selectAll('g')
        .selectAll('path')
        .attr('marker-end', d => {
          // Caption items doesn't have source and target
          if (d.source && d.target && d.source.index === d.target.index) return 'url(#end-self)';
          else return 'url(#end)';
        });

      simulation.alpha(1).restart();
    },
    updateForces() {
      const { simulation, forceProperties, width, height } = this;
      simulation
        .force('center')
        .x(width * forceProperties.center.x)
        .y(height * forceProperties.center.y);
      simulation
        .force('charge')
        .strength(forceProperties.charge.strength * forceProperties.charge.enabled)
        .distanceMin(forceProperties.charge.distanceMin)
        .distanceMax(forceProperties.charge.distanceMax);
      simulation
        .force('collide')
        .strength(forceProperties.collide.strength * forceProperties.collide.enabled)
        .radius(forceProperties.collide.radius)
        .iterations(forceProperties.collide.iterations);
      simulation
        .force('forceX')
        .strength(forceProperties.forceX.strength * forceProperties.forceX.enabled)
        .x(width * forceProperties.forceX.x);
      simulation
        .force('forceY')
        .strength(forceProperties.forceY.strength * forceProperties.forceY.enabled)
        .y(height * forceProperties.forceY.y);
      simulation
        .force('link')
        .distance(forceProperties.link.distance)
        .iterations(forceProperties.link.iterations);

      // updates ignored until this is run
      // restarts the simulation (important if simulation has already slowed down)
      simulation.alpha(1).restart();
    },
  },
  watch: {
    data: {
      handler(newData) {
        this.updateData();
      },
      deep: true,
    },
    forceProperties: {
      handler(newForce) {
        this.updateForces();
      },
      deep: true,
    },
  },
};
</script>

<style lang="scss">
.dependency-test {
  path.link {
    fill: none;
    stroke: #666;
    stroke-width: 1.5px;
  }
  path.link.depends {
    stroke: #005900;
    stroke-dasharray: 5, 2;
  }
  path.link.needs {
    stroke: #7f3f00;
  }

  circle {
    fill: #ffff99;
    stroke: #191900;
    stroke-width: 1.5px;
  }
  circle.system {
    fill: #cce5ff;
    stroke: #003366;
  }
  circle.mount {
    fill: #ffe5e5;
    stroke: #660000;
  }
  circle.init {
    fill: #b2e8b2;
    stroke: #001900;
  }

  text {
    font: 10px sans-serif;
    pointer-events: none;
    text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
  }
}
</style>
