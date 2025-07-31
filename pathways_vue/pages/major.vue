// major.vue
<template>
  <Layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="d-flex flex-column">
        <div v-if="major_data" class="row order-2 justify-content-sm-center">
          <div class="col-md-9">
            <major-details :major="major_data" />
            <explore-major :major="major_data" />
          </div>
          <div class="col-md-9">
            <d3-cgpa :major-data="major_data" />
          </div>
          <div class="col-md-9">
            <common-courses :major="major_data" />
          </div>
          <div class="col-md-9">
            <similar-major :similar-major-data="major_data.similar_majors" />
          </div>
          <div class="col-md-9">
            <contact-adviser
              :campus="major_data.major_campus"
              :type="'major'"
            />
          </div>
        </div>
        <div v-else class="row order-2 justify-content-sm-center">
          <div v-if="showError" class="col-md-9">
            <div class="alert alert-purple" role="alert">
              <p>
                Data is not available for selected major. Here are some possible
                reasons:
              </p>
              <ul>
                <li>This major is no longer offered</li>
                <li>It is a graduate degree</li>
                <li>You made a typo -- the major doesn't exist.</li>
              </ul>
            </div>
          </div>
          <div v-else class="col-md-9 text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>

        <div class="order-1 row justify-content-center">
          <div class="col-md-9">
            <SearchComponent />
          </div>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import Layout from "@/layout.vue";
import MajorDetails from "@/components/major/major-details.vue";
import ExploreMajor from "@/components/major/explore-major.vue";
import CommonCourses from "@/components/major/common-courses.vue";
import D3Cgpa from "@/components/major/d3-cgpa.vue";
import ContactAdviser from "@/components/common/contact-adviser.vue";
import utils from "@/utils.js";
import { useCustomFetch } from "@/composables/customFetch";
import SimilarMajor from "@/components/major/similar-major.vue";
import SearchComponent from "@/components/search/search.vue";

export default {
  name: "MajorComp",
  components: {
    Layout,
    SearchComponent,
    "d3-cgpa": D3Cgpa,
    "contact-adviser": ContactAdviser,
    "major-details": MajorDetails,
    "explore-major": ExploreMajor,
    "common-courses": CommonCourses,
    "similar-major": SimilarMajor,
  },
  data() {
    return {
      selectedMajor: undefined,
      majorID: undefined,
      majorTitle: undefined,
      major_data: undefined,
      showError: false,
      appName: "DawgPath",
    };
  },
  computed: {
    pageTitle: function () {
      let no_title = this.showError ? "Error" : "Major";
      return this.majorTitle !== undefined
        ? (document.title = this.majorTitle + " - " + this.appName)
        : no_title;
    },
  },
  methods: {
    switch_major(data) {
      this.majorID = data.id;
      this.campus = data.campus;
    },
    get_major_data() {
      const vue = this;
      this.major_data = undefined;
      if (this.majorID !== undefined) {
        this.axios
          .get("/api/v1/majors/details/" + this.majorID)
          .then((response) => {
            vue.major_data = response.data;
            vue.majorTitle = vue.major_data.credential_title;
            vue.showError = false;
            vue.recentViewManager(
              vue.majorTitle,
              "major?id=" + vue.majorID,
              vue.major_data.major_campus
            );
          })
          .catch(function () {
            vue.showError = true;
          });
      } else {
        this.showError = true;
      }
    },
  },
  mounted() {
    this.majorID = this.$route.query.id;
  },
  watch: {
    majorID() {
      this.get_major_data();
    },
  },
  created() {
    this.recentViewManager = utils.recentViewManager;
  },
  methods: {
    switch_major(data) {
      this.majorID = data.id;
      this.campus = data.campus;
    },
    async get_major_data() {
      this.major_data = undefined;

      if (this.majorID !== undefined) {
        try {
          const data = await useCustomFetch(
            "/api/v1/majors/details/" + this.majorID
          );
          this.major_data = data;
          this.majorTitle = data.credential_title;
          this.showError = false;
          this.recentViewManager(
            this.majorTitle,
            "major?id=" + this.majorID,
            data.major_campus
          );
        } catch (error) {
          this.showError = true;
        }
      } else {
        this.showError = true;
      }
    },
  },
};
</script>
