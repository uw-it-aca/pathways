// major.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <d3-boxplot />
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';

export default {
  components: {
    layout: Layout,
    'd3-boxplot': D3BoxPlot
  },
  data() {
    return {
      pageTitle: 'Major',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
