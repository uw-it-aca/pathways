// explore-major.vue

<template>
  <ul class="nav mb-5">
    <!--<li v-if="major['major_home_url']">
          <a :href="major['major_home_url']" target="_blank">Degree Requirements</a>
    </li>-->
    <li class="nav-item me-5" v-if="major['program_code']">
      <a class="nav-link p-0" :href="myplanProgramURL">MyPlan Program Page</a>
    </li>
    <li class="nav-item" v-if="major['credential_code']">
      <a class="nav-link p-0" :href="myplanCredentialURL">MyPlan Degree Requirements</a>
    </li>
    <li class="nav-item" v-if="major['career_center_major']">
      <a class="nav-link p-0" :href="careerCenterOutcomeURL">Career Center Outcomes</a>
    </li>
  </ul>
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
</style>
