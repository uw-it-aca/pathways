// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <div class="card mb-3 bg-dark hover:bg-danger">
        <div class="card-body">asldkjfas</div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <div class="card mb-3 bg-dark">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3 border-white hover:border">
            <div class="card-body">asldkjfas</div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Getting started',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
