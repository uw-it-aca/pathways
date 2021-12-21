// explore-major.vue

<template>
  <div class="card mb-5">
    <div class="card-body explore-major">
      <h3>Explore this major</h3>
      <ul>
        <!--<li v-if="major['major_home_url']">
          <a :href="major['major_home_url']" target="_blank">Degree Requirements</a>
        </li> -->
        <li v-if="major['program_code']">
          <a :href="myplanProgramURL" target="_blank">MyPlan Program Page</a>
        </li>
        <li v-if="major['credential_code']">
          <a :href="myplanCredentialURL" target="_blank">MyPlan Credential Page</a>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ExploreMajor',
  props: {
    major: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {};
  },
  computed: {
    myplanProgramURL() {
      if(this.major['program_code'] !== null){
        return "https://myplan.uw.edu/program/#/programs/" + this.major['program_code']
      }
    },
    myplanCredentialURL() {
      if(this.major['credential_code'] !== null){
        return "https://myplan.uw.edu/program/#/programs/" + this.major['program_code'] + "/" + this.major['credential_code']
      }
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
</style>
