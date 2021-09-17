// prereq-map.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Prerequisite Map</h3>
      <ul class="nav nav-tabs" id="PrereqMapTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            class="nav-link active"
            data-bs-target="#pm-course"
            id="course-tab"
            data-bs-toggle="tab"
            type="button"
            role="tab"
            aria-controls="course-map"
            aria-selected="true"
          >
            {{ selected }}
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button
            class="nav-link"
            data-bs-target="#pm-curriculum"
            id="curriculum-tab"
            data-bs-toggle="tab"
            type="button"
            role="tab"
            aria-controls="curriculum-map"
            aria-selected="true"
          >
            All CHEM Courses
          </button>
        </li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane w-75 active" id="pm-course" role="tabpanel" aria-labelledby="course-tab">
          <prereq-course />
        </div>
        <div class="tab-pane w-75" id="pm-curriculum" role="tabpanel" aria-labelledby="curriculum-tab">
          <prereq-curriculum />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PrereqCourse from './prereq-course.vue'
import PrereqCurriculum from './prereq-curriculum.vue'

export default {
  name: 'PrereqMap',
  props: { 
    selected: {
      type: String,
    },
  },
  components: {
    'prereq-course': PrereqCourse,
    'prereq-curriculum': PrereqCurriculum,
    },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss"></style>