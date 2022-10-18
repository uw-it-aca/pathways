// explore-course.vue

<template>
  <div class="mb-5">
    <a :href="myplanURL">MyPlan Course Page</a>
  </div>
</template>


<script>
export default {
  name: 'ExploreCourse',
  data() {
    return {};
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  computed: {
    myplanURL() {
      if (this.course['course_id'] !== null) {
        return "https://myplan.uw.edu/course/#/courses/" + encodeURIComponent(this.course['course_id']);
      }
    },
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
