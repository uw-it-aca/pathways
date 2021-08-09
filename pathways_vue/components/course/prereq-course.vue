// prereq-course.vue 

<template>
  <div class="p-3">
    <div class="form-check form-switch">
      <input
        class="form-check-input"
        type="checkbox"
        v-model="viewCourseList"
        id="ToggleCourseList"
      />
      <label class="form-check-label" for="ToggleCourseList">View CHEM 162 prereqs as a list</label>
    </div>
  </div>
  <prereq-course-list v-if="viewCourseList" />
  <div class="card shadow-sm" id="ViewCourseMap" v-else>
    <div class="text-dark p-3 bg-light rounded-top rounded-sm">
      <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
    </div>
  </div>
</template>

<script>
import PrereqCourseList from './prereq-course-list.vue';

export default {
  name: 'PrereqCourse',
  components: {
    'prereq-course-list': PrereqCourseList,
  },
  data() {
    return {
      viewCourseList: false,
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>