<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <template v-if="major_data">
        <div class="row mt-5">
          <div class="col-lg-4 col-12"><SearchMini /></div>
          <div class="order-md-first col-lg-8 col-12">
            <h1
              class="fs-2 fw-semibold ff-encode-sans my-md-0 my-3"
              data-clarity-unmask="true"
            >
              {{ major_data.credential_title }}
            </h1>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-8 col-12">
            <MajorDetails :major="major_data" />
            <ExploreMajor :major="major_data" />
            <D3Cgpa :major-data="major_data" />
            <SimilarMajor :similar-major-data="major_data.similar_majors" />
          </div>
          <div class="col-lg-4 col-12">
            <CommonCourses :major="major_data" />
            <ContactAdviser :campus="major_data.major_campus" :type="'major'" />
          </div>
        </div>
      </template>
      <template v-else>
        <div class="row justify-content-center">
          <div v-if="showError" class="col col-lg-8">
            <div class="alert alert-purple" role="alert">
              <p>Data is not available for selected major. Here are some possible reasons:</p>
              <ul>
                <li>This major is no longer offered</li>
                <li>It is a graduate degree</li>
                <li>You made a typo -- the major doesn't exist.</li>
              </ul>
            </div>
          </div>
          <div v-else-if="loading" class="col col-lg-8 text-center">
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
  import { defineAsyncComponent } from "vue";
  import DefaultLayout from "@/layouts/default.vue";
  import MajorDetails from "@/components/major/major-details.vue";
  import ExploreMajor from "@/components/major/explore-major.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import ContactAdviser from "@/components/common/contact-adviser.vue";
  import utils from "@/utils.js";
  import { useCustomFetch } from "@/composables/customFetch";

  // Lazy-load heavy below-the-fold components so they are code-split into
  // separate chunks and only downloaded/parsed after major data has loaded.
  const D3Cgpa = defineAsyncComponent(() => import("@/components/major/d3-cgpa.vue"));
  const SimilarMajor = defineAsyncComponent(() => import("@/components/major/similar-major.vue"));
  const CommonCourses = defineAsyncComponent(() => import("@/components/major/common-courses.vue"));

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
        majorID: undefined,
        majorTitle: undefined,
        major_data: undefined,
        showError: false,
        loading: false,
      };
    },
    computed: {
      pageTitle() {
        if (this.majorTitle) return this.majorTitle;
        return this.showError ? "Error" : "Major";
      },
    },
    watch: {
      majorTitle(val) {
        if (val) document.title = val + " - DawgPath";
      },
      majorID() {
        this.get_major_data();
      },
    },
    mounted() {
      this.majorID = this.$route.query.id;
    },
    methods: {
      async get_major_data() {
        if (!this.majorID) {
          this.showError = true;
          return;
        }
        this.major_data = undefined;
        this.showError = false;
        this.loading = true;
        try {
          const data = await useCustomFetch("/api/v1/majors/details/" + this.majorID);
          this.major_data = data;
          this.majorTitle = data.credential_title;
          utils.recentViewManager(this.majorTitle, "major?id=" + this.majorID, data.major_campus);
        } catch {
          this.showError = true;
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>
