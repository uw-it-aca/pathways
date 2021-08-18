// explore-course.vue 

<template>
  <div class="card mb-5">
    <div class="card-body explore-course">
      <h3>Explore this Course</h3>
      <ul>
        <li><a href="#">MyPlan Course Page</a></li>
      </ul>
    </div>
  </div>
</template>


<script>
export default {
  name: 'ExploreCourse',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.explore-course {
  ul {
    padding-left: 0;
  }
  li {
    list-style-type: none;
    padding-bottom: 0.5rem;
  }
}
</style>