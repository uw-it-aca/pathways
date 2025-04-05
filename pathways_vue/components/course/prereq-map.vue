// prereq-map.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Prerequisite Map</h2>
      <ul id="PrereqMapTab" class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            id="course-tab"
            class="nav-link active"
            data-bs-target="#pm-course"
            data-bs-toggle="tab"
            type="button"
            role="tab"
            aria-controls="course-map"
            aria-selected="true"
          >
            {{ active_course }}
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button
            id="curriculum-tab"
            class="nav-link"
            data-bs-target="#pm-curriculum"
            data-bs-toggle="tab"
            type="button"
            role="tab"
            aria-controls="curriculum-map"
            aria-selected="true"
          >
            All {{ active_dept }} courses
          </button>
        </li>
      </ul>
      <div class="tab-content">
        <div
          id="pm-course"
          class="tab-pane active"
          role="tabpanel"
          aria-labelledby="course-tab"
        >
          <div v-if="prereq_string">
            <p class="mt-4">
              <strong>Prerequisite: </strong> {{ prereq_string }}
            </p>
          </div>
          <prereq-course
            :graph-data="graphData"
            :active-course="activeCourse"
          />
        </div>
        <div
          id="pm-curriculum"
          class="tab-pane"
          role="tabpanel"
          aria-labelledby="curriculum-tab"
        >
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
import PrereqCourse from "@/components/course/prereq-course.vue";
import PrereqCurriculum from "@/components/course/prereq-curriculum.vue";

export default {
  name: "PrereqMap",
  components: {
    "prereq-course": PrereqCourse,
    "prereq-curriculum": PrereqCurriculum,
  },
  props: {
    graphData: {
      type: Object,
      required: true,
    },
    prereqString: {
      type: String,
      required: false,
      default: "",
    },
    activeCourse: {
      type: String,
      required: true,
    },
  },

  data() {
    return {};
  },
  computed: {
    active_dept: function () {
      let activeCourse = "";
      if (this.active_course) {
        var split_pos = this.active_course.lastIndexOf(" ");
        activeCourse = this.active_course.substring(0, split_pos);
      }
      return activeCourse;
    },
  },
  methods: {},
};
</script>
