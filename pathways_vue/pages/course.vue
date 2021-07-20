// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <div>
        <h2>CHEM 162: General Chemistry</h2>
        <div>Credits: 5</div>
      </div>

      <div class="card mb-5">
        <div class="card-body">Course Grade Distribution</div>
      </div>

      <d3-arc />
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import D3Arc from '../components/d3-arc.vue';

export default {
  components: {
    layout: Layout,
    'd3-arc': D3Arc,
  },
  data() {
    return {
      pageTitle: 'Course',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
