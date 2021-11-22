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
      <label class="form-check-label" for="ToggleCourseList">View {{active_course}} prereqs as a list</label>
    </div>
  </div>
  <prereq-course-list v-if="viewCourseList"
    :graph_data="graph_data"
    :active_course="active_course"
  />
  <div class="card shadow-sm" id="ViewCourseMap" v-else>
    <prereq-graph
      :graph_data="graph_data"
      graph_type="course"
      :active_course="active_course"
    />
    <div class="text-dark p-3 bg-light rounded-top rounded-sm">
      <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
    </div>
  </div>
</template>

<script>
import PrereqCourseList from './prereq-course-list.vue';
import PrereqGraph from './prereq-graph.vue';

export default {
  name: 'PrereqCourse',
  components: {
    PrereqGraph,
    'prereq-course-list': PrereqCourseList,
  },
  data() {
    return {
      viewCourseList: false,
    };
  },
  props: {
    graph_data: {
      type: Object,
      required: true,
    },
    active_course: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss"></style>
