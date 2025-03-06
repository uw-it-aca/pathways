<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Similar Majors</h2>
      <div>
        Topically similar majors are determined through several sources, including major and course descriptions. Explore majors and concentrations that align with your interests and strengths.
        <a href="#" v-on:click.prevent="showHelpModal">About Topically Similar Majors</a>
      </div>
      <div>
        <similar-major-row
          v-for="(major, index) in similarMajorData"
          :key="index"
          :majorData="major"
          />
      </div>
    </div>
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
      helpModal: undefined
    };
  },
  methods: {
    showHelpModal() {
      this.helpModal = new Modal(document.getElementById("help_modal"), {});
      this.helpModal.show();
    },
  },
  computed: {},
};
</script>
