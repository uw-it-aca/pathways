// explore-major.vue 

<template>
  <div class="card mb-5">
    <div class="card-body explore-major">
      <h3>Explore this Major</h3>
      <ul>
        <!-- TODO: improve this to have proper capitalization and key/value mapping -->
        <li v-for="(field, i) in fields" :key="i">
          <a :href="major[field]">{{ field }}</a>
        </li>
        <li><a href="#">MyPlan Program Page</a></li>
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
    fields() {
      let wantedFields = [
        'Degree requirements',
      ];

      return wantedFields.filter((field) => field in this.major);
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