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
          class="form-check-input"
          type="checkbox"
          v-model="viewCourseList"
          id="ToggleCourseList"
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
    <div class="card shadow-sm" id="ViewCourseMap" v-else>
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
