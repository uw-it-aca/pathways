// explore-major.vue

<template>
  <h2 class="h4 axdd-font-encode-sans fw-bold mb-3">Explore this Major</h2>
  <div class="row mb-5">
    <div class="col-md-4 mb-3" v-if="major['program_code']">
      <a class="card-link p-0 text-decoration-none" :href="myplanProgramURL">
        <div class="card h-100">
          <div class="card-body d-flex">
            <div class="pe-2">
              <i class="bi-journal-bookmark display-5 text-purple"></i>
            </div>
            <div class="">
              <h3 class="h6 card-title mb-0 text-dark">
                <strong>Program Information</strong>
              </h3>
              <small>
                <p class="card-text text-dark p-0">
                  Learn more about this program and its degrees
                </p>
              </small>
            </div>
          </div>
        </div>
      </a>
    </div>
    <div class="col-md-4 mb-3" v-if="major['credential_code']">
      <a class="card-link p-0 text-decoration-none" :href="myplanCredentialURL">
        <div class="card h-100">
          <div class="card-body d-flex">
            <div class="pe-2">
              <i class="bi-clipboard-check display-5 text-purple"></i>
            </div>
            <div class="">
              <h3 class="h6 card-title mb-0 text-dark">
                <strong>Degree Requirements</strong>
              </h3>
              <small>
                <p class="card-text p-0 text-dark">
                  Review courses needed to complete this degree
                </p>
              </small>
            </div>
          </div>
        </div>
      </a>
    </div>
    <div class="col-md-4 mb-3" v-if="major['career_center_major']">
      <a
        class="card-link p-0 text-decoration-none"
        :href="careerCenterOutcomeURL"
      >
        <div class="card h-100">
          <div class="card-body d-flex">
            <div class="pe-2">
              <span class="material-symbols-outlined display-4 text-purple">
                donut_small
              </span>
            </div>
            <div class="">
              <h3 class="h6 card-title mb-0 text-dark">
                <strong>Career Outcomes</strong>
              </h3>
              <small>
                <p class="card-text p-0 text-dark">
                  Explore what UW graduates do with this degree
                </p>
              </small>
            </div>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExploreMajor",
  props: {
    major: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    myplanProgramURL() {
      let url = "";
      if (this.major["program_code"] !== null) {
        url =
          "https://myplan.uw.edu/program/#/programs/" +
          this.major["program_code"];
      }
      return url;
    },
    myplanCredentialURL() {
      let url = "";
      if (this.major["credential_code"] !== null) {
        url =
          "https://myplan.uw.edu/program/#/programs/" +
          this.major["program_code"] +
          "/" +
          this.major["credential_code"];
      }
      return url;
    },
    careerCenterOutcomeURL() {
      let url = "";
      if (this.major["career_center_major"] !== null) {
        url =
          "https://careers.uw.edu/outcomes/#!" +
          this.major["career_center_major"];
      }
      return url;
    },
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.explore-major {
  ul {
    padding-left: 0;
  }

  li {
    list-style-type: none;
    padding-bottom: 0.5rem;
  }
}

.material-symbols-outlined {
  top: 1rem;
}

@media (max-width: 767.98px) {
  .material-symbols-outlined {
    top: 0.4rem;
  }
}

.card:hover {
  opacity: 0.7;
  -khtml-opacity: 0.7;
}
</style>
