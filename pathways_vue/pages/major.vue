// major.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <template v-if="major_data">
        <div class="row justify-content-center border-success order-2 border">
          <div class="col col-md-9">
            <MajorDetails :major="major_data" />
            <ExploreMajor :major="major_data" />
            <D3Cgpa :major-data="major_data" />
            <CommonCourses :major="major_data" />
            <SimilarMajor :similar-major-data="major_data.similar_majors" />
            <ContactAdviser :campus="major_data.major_campus" :type="'major'" />
          </div>
        </div>
      </template>
      <template v-else>
        <div class="row justify-content-center border-danger border">
          <div v-if="showError" class="col col-md-9">
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
          <div v-else class="col col-md-9 border-danger border text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </template>
      <div class="row justify-content-center border-warning order-1 border">
        <div class="col col-md-9">
          <Search />
        </div>
      </div>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import MajorDetails from "@/components/major/major-details.vue";
  import ExploreMajor from "@/components/major/explore-major.vue";
  import CommonCourses from "@/components/major/common-courses.vue";
  import Search from "@/components/search/search.vue";
  import D3Cgpa from "@/components/major/d3-cgpa.vue";
  import ContactAdviser from "@/components/common/contact-adviser.vue";
  import SimilarMajor from "@/components/major/similar-major.vue";
  import utils from "@/utils.js";

  export default {
    name: "MajorComp",
    components: {
      DefaultLayout,
      Search,
      D3Cgpa,
      ContactAdviser,
      MajorDetails,
      ExploreMajor,
      CommonCourses,
      SimilarMajor,
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
    created() {
      this.recentViewManager = utils.recentViewManager;
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
                vue.major_data.major_campus,
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
  };
</script>
