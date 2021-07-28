// prereq-course.vue 

<template>
  <div class="p-3">
    <div class="form-check form-switch">
      <label class="form-check-label" for="ViewCourseList">View as a list</label>
      <input class="form-check-input" type="checkbox" id="ViewCourseList" />
    </div>
  </div>
  <div class="card shadow-sm">
    <div class="text-dark p-3 bg-light rounded-top rounded-sm">
      <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrereqCourse',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss"></style>