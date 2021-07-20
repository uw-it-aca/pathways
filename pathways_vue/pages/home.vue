// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <div class="card mb-3 bg-light">
        <div class="card-body"><hello-world /></div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <div class="card mb-3 bg-light">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3 border-white">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
      </div>
      <div class="card mb-3 bg-light">
        <div class="card-body">
          <d3-arc />
        </div>
      </div>
      <div class="card mb-3 bg-light">
        <div class="card-body">
          <d3-boxplot />
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import HelloWorld from '../components/hello-world.vue';
import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';

export default {
  components: {
    layout: Layout,
    'hello-world': HelloWorld,
    'd3-arc': D3Arc,
    'd3-boxplot': D3BoxPlot
  },
  data() {
    return {
      pageTitle: 'My Home Page',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
