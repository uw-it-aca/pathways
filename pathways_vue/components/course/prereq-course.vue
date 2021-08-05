// prereq-course.vue 

<template>
  <div class="p-3">
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" v-model="viewList" id="ViewCourseList" />
      <label class="form-check-label" for="ViewCourseList">View as a list</label>
    </div>
  </div>
  <prereq-course-list v-if="viewList"/>
  <div class="card shadow-sm" id="ViewMap" v-else>
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
      viewList: false,
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>