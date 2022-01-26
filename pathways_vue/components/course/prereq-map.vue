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
            {{active_course}}
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
            All {{active_dept}} courses
          </button>
        </li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane active" id="pm-course" role="tabpanel" aria-labelledby="course-tab">
          <prereq-course
            :graph_data="graph_data"
            :active_course="active_course"
          />
        </div>
        <div class="tab-pane" id="pm-curriculum" role="tabpanel" aria-labelledby="curriculum-tab">
          <prereq-curriculum
            :curric_id="active_dept"
            :course_id="active_course"
          />
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
  components: {
    'prereq-course': PrereqCourse,
    'prereq-curriculum': PrereqCurriculum,
    },
  data() {
    return {};
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
  computed: {
    active_dept: function (){
      if(this.active_course){
        var split_pos = this.active_course.lastIndexOf(" ");
        return this.active_course.substring(0, split_pos);
      }
    }
  },
  methods: {},
};
</script>

<style lang="scss"></style>
