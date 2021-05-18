// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <div class="card mb-3 bg-light">
        <div class="card-body">asldkjfas</div>
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
          <d3-test />
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import D3Test from '../components/d3-test.vue';

export default {
  components: {
    layout: Layout,
    'd3-test': D3Test,
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
