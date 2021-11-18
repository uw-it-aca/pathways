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
          <search-major
            :prefill_id="majorID"
          />
        </div>
      </div>
      <div v-if="major_data">
        <div class="row">
          <div class="col-sm-8"><major-details :major="major_data" /></div>
          <div class="col-sm-4"><explore-major :major="major_data" /></div>
        </div>
        <div class="mb-5">
          <common-courses :major="major_data" />
        </div>
        <div class="row">
          <div class="col-sm-8"><d3-cgpa :major-data="major_data"/></div>
          <div class="col-sm-4"></div>
        </div>
        
        <contact-adviser-major />
      </div>
      <div v-else>
        No major selected
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
import D3Cgpa from '../components/major/d3-cgpa.vue';
import ContactAdviserMajor from '../components/major/contact-adviser-major.vue';

export default {
  components: {
    'layout': Layout,
    'search-major': SearchMajor,
    'd3-cgpa': D3Cgpa,
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
    this.emitter.on("update:selected", selectedKey => {
      this.majorID = selectedKey;

    })
  },
  watch: {
    majorID(newValue) {
      this.get_major_data(newValue);
    }
  },
};
</script>

<style lang="scss"></style>
