// explore-major.vue 

<template>
  <div class="card mb-5">
    <div class="card-body explore-major">
      <h3>Explore this Major</h3>
      <ul>
        <li><a href="#">Admission Requirements</a></li>
        <li><a href="#">MyPlan Program Page</a></li>
      </ul>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ExploreMajor',
  data() {
    return {};
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