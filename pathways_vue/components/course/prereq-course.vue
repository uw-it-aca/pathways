// prereq-course.vue

<template>
  <div v-if="graph_data == null" class="p-3">
    <div class="alert alert-purple" role="alert">
      <p>
        The course
        <strong>{{ active_course }}</strong> does not have prereqs and is not a
        prereq for other courses.
      </p>
    </div>
  </div>
  <div v-else>
    <div class="p-3">
      <div class="form-check form-switch">
        <input
          id="ToggleCourseList"
          v-model="viewCourseList"
          class="form-check-input"
          type="checkbox"
        />
        <label class="form-check-label" for="ToggleCourseList"
          >View {{ active_course }} prereqs as a list</label
        >
      </div>
    </div>
    <prereq-course-list
      v-if="viewCourseList"
      :graph_data="graph_data"
      :active_course="active_course"
    />
    <div v-else id="ViewCourseMap" class="card shadow-sm">
      <prereq-graph
        :graph_data="graph_data"
        graph_type="course"
        :active_course="active_course"
      />
      <div class="text-dark p-3 bg-light rounded-top rounded-sm">
        <small
          >Use the scroll function on your mouse or touchpad to zoom in and
          out</small
        >
      </div>
    </div>
  </div>
</template>

<script>
import PrereqCourseList from "@/components/course/prereq-course-list.vue";
import PrereqGraph from "@/components/course/prereq-graph.vue";

export default {
  name: "PrereqCourse",
  components: {
    PrereqGraph,
    "prereq-course-list": PrereqCourseList,
  },
  props: {
    graphData: {
      type: Object,
      required: true,
    },
    activeCourse: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      viewCourseList: false,
    };
  },
  computed: {
    show_graph: function () {
      if (this.graph_data && this.graph_data.x) {
        return Object.keys(this.graph_data.x.edges.from).length > 0;
      }
      return false;
    },
  },
};
</script>
