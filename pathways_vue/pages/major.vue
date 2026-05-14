// major.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <template v-if="major_data">
        <div class="row mt-5">
          <div class="col-md-4 col-12"><SearchMini /></div>
          <div class="order-md-first col-md-8 col-12">
            <h1
              class="fs-2 fw-semibold ff-encode-sans my-md-0 my-3"
              data-clarity-unmask="true"
            >
              {{ major_data["credential_title"] }}
            </h1>
          </div>
        </div>

        <div class="row">
          <div class="col-md-8 col-12">
            <MajorDetails :major="major_data" />
            <ExploreMajor :major="major_data" />
            <D3Cgpa :major-data="major_data" />
            <SimilarMajor :similar-major-data="major_data.similar_majors" />
          </div>
          <div class="col-md-4 col-12">
            <CommonCourses :major="major_data" />
            <ContactAdviser :campus="major_data.major_campus" :type="'major'" />
          </div>
        </div>
      </template>
      <template v-else>
        <div class="row justify-content-center">
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
          <div v-else class="col col-md-9 text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </template>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import MajorDetails from "@/components/major/major-details.vue";
  import ExploreMajor from "@/components/major/explore-major.vue";
  import CommonCourses from "@/components/major/common-courses.vue";
  import D3Cgpa from "@/components/major/d3-cgpa.vue";
  import ContactAdviser from "@/components/common/contact-adviser.vue";
  import SimilarMajor from "@/components/major/similar-major.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import utils from "@/utils.js";
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "MajorComp",
    components: {
      DefaultLayout,
      D3Cgpa,
      ContactAdviser,
      MajorDetails,
      ExploreMajor,
      CommonCourses,
      SimilarMajor,
      SearchMini,
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
      async get_major_data() {
        this.major_data = undefined;
        if (this.majorID !== undefined) {
          try {
            const data = await useCustomFetch(
              "/api/v1/majors/details/" + this.majorID,
            );
            this.major_data = data;
            this.majorTitle = this.major_data.credential_title;
            this.showError = false;
            this.recentViewManager(
              this.majorTitle,
              "major?id=" + this.majorID,
              this.major_data.major_campus,
            );
          } catch (error) {
            this.showError = true;
          }
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
