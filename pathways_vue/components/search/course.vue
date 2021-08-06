// course.vue

<template>
  <search
    inner-id="courses"
    :options="courseListSearchable"
    placeholder="Enter a course code"
    route-path="course"
    sync-query-param="code"
    v-model:selected="selected"
  />
</template>

<script>
import Search from './search.vue';

export default {
  name: 'SearchCourse',
  components: {
    'search': Search,
  },
  props: {
    courseList: {
      type: Array,
      required: true,
    },
    selected: String,
  },
  emits: ['update:selected'],
  computed: {
    courseListSearchable() {
      let selectable = {};

      this.courseList.forEach((course) => {
        selectable[course.trim()] = course;
      });

      return selectable;
    }
  },
  watch: {
    selected(newValue) {
      this.$emit('update:selected', newValue);
    }
  },
};
</script>

<style lang="scss"></style>
