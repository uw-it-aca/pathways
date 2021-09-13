// major.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>
    <template #content>

      <div class="row justify-content-center mb-5">
        <div class="col-md-9">
<!--          <search-major v-model:selected="majorID" :prefill_id="majorID"/>-->
        </div>
      </div>
      <div v-if="major_data">
        <div class="row">
<!--          <div class="col-8"><major-details :major="selectedMajor" /></div>-->
<!--          <div class="col-4"><explore-major :major="selectedMajor" /></div>-->
        </div>
        <div class="mb-5">
<!--          <common-courses />-->
        </div>

        <d3-histogram
          :major-data="major_data"
        />
<!--        <contact-adviser />-->
      </div>
      <div v-else>
        PLACEHOLDER: select something |{{majorID}}|
      </div>
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
      selectedMajor: null,
      majorID: null,
      major_data: null
    };
  },
  methods: {
    get_major_data(major_id){
      const vue = this;
      this.axios.get("/api/v1/majors/" + major_id).then((response) => {
        vue.major_data = response.data;
      });
    }

  },
  mounted(){
    let major_id = this.$route.query.id;
    this.majorID = major_id;
    this.get_major_data(major_id);
  }
};
</script>

<style lang="scss"></style>
