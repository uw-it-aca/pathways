// explore-major.vue

<template>
  <h2 class="h4 pw-font-encode-sans mb-3">Explore this Major</h2>
  <div class="row mb-5">
    <div class="col-sm-4" v-if="major['program_code']">
      <div class="card">
        <div class="card-body d-flex">
          <div class="pe-2"><i class="bi bi-journal-bookmark display-5 text-purple"></i></div>
          <div class="">
            <h3 class="h6 card-title mb-0"><a class="nav-link p-0" :href="myplanProgramURL">Program Information</a></h3>
            <small><p class="card-text p-0">Learn more about this program and its degrees</p></small>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-4" v-if="major['credential_code']">
      <div class="card">
        <div class="card-body d-flex">
          <div class="pe-2"><i class="bi bi-clipboard-check display-5 text-purple"></i></div>
          <div class="">
          <h3 class="h6 card-title mb-0"><a class="nav-link p-0" :href="myplanCredentialURL">Degree Requirements</a></h3>
          <small><p class="card-text p-0">View courses needed to complete this degree</p></small>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-4" v-if="major['career_center_major']">
      <div class="card">
        <div class="card-body d-flex">
          <div class="pe-2"><span class="material-symbols-outlined display-4 text-purple">
donut_small
</span></div>
          <div class="">
          <h3 class="h6 card-title mb-0"><a class="nav-link p-0" :href="careerCenterOutcomeURL">Career Outcomes</a></h3>
          <small><p class="card-text p-0">See what graduates do with this degree</p></small>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- <ul class="nav mb-5">
    <li class="nav-item me-5" v-if="major['program_code']">
      <a class="nav-link p-0" :href="myplanProgramURL">MyPlan Program Page</a>
    </li>
    <li class="nav-item" v-if="major['credential_code']">
      <a class="nav-link p-0" :href="myplanCredentialURL">MyPlan Degree Requirements</a>
    </li>
    <li class="nav-item" v-if="major['career_center_major']">
      <a class="nav-link p-0" :href="careerCenterOutcomeURL">Career Center Outcomes</a>
    </li>
  </ul> -->
</template>

<script>
export default {
  name: 'ExploreMajor',
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
      if (this.major['program_code'] !== null) {
        return 'https://myplan.uw.edu/program/#/programs/' + this.major['program_code'];
      }
    },
    myplanCredentialURL() {
      if (this.major['credential_code'] !== null) {
        return (
          'https://myplan.uw.edu/program/#/programs/' +
          this.major['program_code'] +
          '/' +
          this.major['credential_code']
        );
      }
    },
    careerCenterOutcomeURL(){
      if (this.major['career_center_major'] !== null) {
        return (
          'https://careers.uw.edu/outcomes/#!' +
          this.major['career_center_major']
        );
      }
    }
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
</style>
