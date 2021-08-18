// major.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="mb-5">
        <search-major v-model:selectedMajor="selectedMajor" :major-list="majorSeaList"/>
      </div>
      <div v-if="selectedMajor">
        <div class="row">
          <div class="col-8"><major-details :major="selectedMajor" /></div>
          <div class="col-4"><explore-major :major="selectedMajor" /></div>
        </div>
        <div class="mb-5">
          <common-courses />
        </div>

        <d3-histogram />
        <contact-adviser />
      </div>
      <div v-else>
        PLACEHOLDER: select something
      </div>
    </template>
  </layout>
</template>

<script>
import majorSeaData from '../data/majors-sea.json';

import { proccessSeaMajors } from '../helpers/major';

import Layout from '../layout.vue';
import MajorDetails from '../components/major/major-details.vue';
import ExploreMajor from '../components/major/explore-major.vue';
import CommonCourses from '../components/major/common-courses.vue';
import SearchMajor from '../components/search/major.vue';
import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';
import D3Histogram from '../components/d3-histogram.vue';
import ContactAdviserMajor from '../components/major/contact-adviser-major.vue';

export default {
  components: {
    'layout': Layout,
    'search-major': SearchMajor,
    'd3-boxplot': D3BoxPlot,
    'd3-histogram': D3Histogram,
    'contact-adviser-major': ContactAdviserMajor,
    'major-details': MajorDetails,
    'explore-major': ExploreMajor,
    'common-courses': CommonCourses,
  },
  data() {
    return {
      pageTitle: 'Major',
      majorSeaList: proccessSeaMajors(majorSeaData),
      selectedMajor: null,
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
