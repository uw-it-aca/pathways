// major.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="mb-5">
        <search-major />
      </div>
        <div class="row">
          <div class="col-8"><major-details /></div>
          <div class="col-4"><explore-major /></div>
        </div>
      <div class="mb-5">
        <common-courses />
      </div>
      
      <d3-histogram />
      <contact-adviser />
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import MajorDetails from '../components/major/major-details.vue';
import ExploreMajor from '../components/major/explore-major.vue';
import CommonCourses from '../components/major/common-courses.vue';
import SearchMajor from '../components/search/major.vue';
import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';
import D3Histogram from '../components/d3-histogram.vue';
import ContactAdviser from '../components/_common/contact-adviser.vue';

export default {
  components: {
    'layout': Layout,
    'search-major': SearchMajor,
    'd3-boxplot': D3BoxPlot,
    'd3-histogram': D3Histogram,
    'contact-adviser': ContactAdviser,
    'major-details': MajorDetails,
    'explore-major': ExploreMajor,
    'common-courses': CommonCourses,
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
