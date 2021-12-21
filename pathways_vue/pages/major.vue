// major.vue
<template>
  <layout v-if="pageTitle !== undefined" :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>
    <template #content>

      <div class="row justify-content-center mb-5">
        <div class="col-md-9">
          <search-chooser
            :prefill-id="majorID"
            :prefill-campus="campus"
            prefill-type="major"
            @update:selected="switch_major"
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

        <contact-adviser :campus="campus" :type="'major'"/>
      </div>
      <div v-else>
        <div v-if="showError">
          <div class="alert alert-info" role="alert">
            <p>Data is not available for selected major. Here are some possible reasons:</p>
            <ul>
              <li>This major is no longer offered</li>
              <li>It is a graduate degree</li>
              <li>You made a typo -- the major doesn’t exist.</li>
            </ul>
          </div>
        </div>
        <div v-else>
          <div class="d-flex justify-content-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>

      </div>
    </template>
  </layout>
</template>

<script>

import Layout from '../layout.vue';
import MajorDetails from '../components/major/major-details.vue';
import ExploreMajor from '../components/major/explore-major.vue';
import CommonCourses from '../components/major/common-courses.vue';
import SearchChooser from "../components/search/chooser.vue";
import D3Cgpa from '../components/major/d3-cgpa.vue';
import ContactAdviser from '../components/common/contact-adviser.vue';

export default {
  components: {
    'layout': Layout,
    'search-chooser': SearchChooser,
    'd3-cgpa': D3Cgpa,
    'contact-adviser': ContactAdviser,
    'major-details': MajorDetails,
    'explore-major': ExploreMajor,
    'common-courses': CommonCourses,
  },
  data() {
    return {
      selectedMajor: null,
      majorID: null,
      majorTitle: undefined,
      campus: null,
      major_data: undefined,
      showError: false
    };
  },
  computed: {
    pageTitle: function() {
      return this.majorTitle;
    }
  },
  methods: {
    switch_major(data){
      this.majorID = data.id;
      this.campus = data.campus
    },
    get_major_data(){
      const vue = this;
      this.major_data = undefined;
      if(this.campus !== null && this.majorID !== null){
        this.axios.get("/api/v1/majors/" + this.campus + "/" + this.majorID).then((response) => {
          vue.major_data = response.data;
          vue.majorTitle = vue.major_data.credential_title + " - Major ";
        }).catch(function (error) {
          vue.showError = true;
        });
      }
    }
  },
  mounted(){
    this.majorID = this.$route.query.id;
    this.campus = this.$route.query.campus;
  },
  watch: {
    majorID() {
      this.get_major_data();
    }
  },
};
</script>

<style lang="scss"></style>
