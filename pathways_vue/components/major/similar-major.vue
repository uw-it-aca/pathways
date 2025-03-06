<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Similar Majors</h2>
      <div>
        Topically similar majors are determined through several sources, including major and course descriptions. Explore majors and concentrations that align with your interests and strengths.
        <a href="#" v-on:click.prevent="showHelpModal">About Topically Similar Majors</a>
      </div>
      <button v-on:click="showFilters"><i class="bi-filter"></i>Filter</button>
      <div>
        <similar-major-row
          v-for="(major, index) in similarMajors"
          :key="index"
          :majorData="major"
          />
      </div>
    </div>
  </div>

  <!-- Filter Box -->
  <div v-if="filtersShown">
    <form>
      <fieldset>
        <legend>Campus</legend>

        <input type="checkbox" id="seattle" value="seattle" v-model="filters.campus">
        <label for="seattle">Seattle</label>

        <input type="checkbox" id="bothell" value="bothell" v-model="filters.campus">
        <label for="bothell">Bothell</label>

        <input type="checkbox" id="tacoma" value="tacoma" v-model="filters.campus">
        <label for="tacoma">Tacoma</label>
      </fieldset>
      <fieldset>
        <legend>Admission Type</legend>

        <input type="checkbox" id="open" value="open" v-model="filters.admissionType">
        <label for="open">Open Admission</label>

        <input type="checkbox" id="minimumRequirements" value="minimumRequirements" v-model="filters.admissionType">
        <label for="minimumRequirements">Minimum Requirements</label>

        <input type="checkbox" id="capacity-constrained" value="capacity-constrained" v-model="filters.admissionType">
        <label for="capacity-constrained">Capacity Constrained</label>
      </fieldset>
      <fieldset>
        <legend>STEM</legend>
        <input type="checkbox" id="stem" value="stem" v-model="filters.stem">
        <label for="stem">STEM Majors</label>

        <input type="checkbox" id="non-stem" value="non-stem" v-model="filters.stem">
        <label for="non-stem">Non-STEM Majors</label>
      </fieldset>
    </form>
  </div>

  <!-- Help Modal -->
  <div
    class="modal fade"
    role="dialog"
    id="help_modal"
    tabindex="-1"
    aria-modal="true"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-body">
          <div>
            <h1>Similar Majors</h1>
            <ul>
              <li>The similarity between majors is gauged by analyzing the overlap in key terminology and subject matter within major and course descriptions. Similarity is not calculated based on career outcome.</li>
              <li>Note that the similar majors listed in this tool are a sampling only, and are not necessarily more valuable than other majors you may wish to explore.</li>
              <li>Deciding on a major is a critical step in your academic journey. Carefully consider your interests, strengths, and long-term career goals. Consulting with an academic adviser can help ensure your chosen major aligns with your interests and goals.</li>
            </ul>
          </div>
          <div class="text-end">
            <button
              type="button"
              class="btn btn-purple text-end"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              Ok, got it
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import SimilarMajorRow from "@/components/major/similar_major_row.vue";

export default {
  name: "SimilarMajor",
  components: {
    SimilarMajorRow,
  },
  props: {
    similarMajorData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      helpModal: undefined,
      filtersShown: false,
      filters: {
        campus: [],
        admissionType: [],
        stem: []
      },
      similarMajors: [],
    };
  },
  watch: {
    filters: {
      handler: function () {
        this.filterMajors();
      },
      deep: true,
    },
  },
  mounted() {
    this.similarMajors = this.similarMajorData;
  },
  methods: {
    showHelpModal() {
      this.helpModal = new Modal(document.getElementById("help_modal"), {});
      this.helpModal.show();
    },
    showFilters() {
      this.filtersShown = !this.filtersShown;
    },
    filterMajors() {
      // Filter similarMajorData based on filters
      let filtered_majors = this.similarMajorData;
      if (this.filters.campus.length > 0 && this.filters.campus.length < 3) {
        filtered_majors = filtered_majors.filter(major => this.filters.campus.includes(major.campus.toLowerCase()));
      }
      if (this.filters.admissionType.length > 0 && this.filters.admissionType.length < 3) {
        filtered_majors = filtered_majors.filter(major => this.filters.admissionType.includes(major.admission));
      }
      if (this.filters.stem.length === 1 ) {
        let isStem = this.filters.stem[0] === 'stem';
        filtered_majors = filtered_majors.filter(major => isStem === major.isStem);
      }
      this.similarMajors = filtered_majors;
    },
  },
  computed: {},
};
</script>
