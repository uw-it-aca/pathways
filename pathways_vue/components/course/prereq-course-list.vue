//prereq-course-list.vue

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h3>
        Prerequisites for {{ active_course }}
        <span class="badge rounded-pill bg-purple">{{ prereqs.length }}</span>
      </h3>
      <div class="mt-3">
        <ul class="list-unstyled mb-0">
          <li v-for="(prereq, index) in prereqs" :key="index">
            <a :href="'/course?id=' + prereq.course_id" class="d-block mb-3">
              {{ prereq.course_id }}: {{ prereq.course_title }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="card mb-3">
    <div class="card-body">
      <h3>
        {{ active_course }} is a prerequisite for
        <span class="badge rounded-pill bg-purple">{{ postreqs.length }}</span>
      </h3>
      <small
        >Some courses may require multiple prerequisites before
        completion.</small
      >
      <div class="mt-3">
        <ul class="list-unstyled mb-0">
          <li v-for="(postreq, index) in postreqs" :key="index">
            <h4 class="fs-6">
              <a
                :href="'/course?id=' + postreq.course_id"
                class="d-block mb-3"
                :title="
                  'Go to course ' +
                  postreq.course_id +
                  ' ' +
                  postreq.course_title
                "
              >
                {{ postreq.course_id }}: {{ postreq.course_title }}
              </a>
            </h4>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PrereqCourseList",
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
      prereqs: [],
      postreqs: [],
    };
  },
  computed: {},
  mounted() {
    this.build();
  },
  methods: {
    build: function () {
      this.prereqs = this.get_courses_from_list(
        this.active_course,
        this.graphData.x.edges.from
      );
      this.postreqs = this.get_courses_from_list(
        this.active_course,
        this.graphData.x.edges.to
      );
    },
    get_courses_from_list(current_course, list) {
      var values = [...new Set(Object.values(list))];
      var vue = this;
      var new_list = [];
      values.forEach(function (course) {
        if (current_course !== course && !new_list.includes(course)) {
          new_list.push({
            course_id: course,
            course_title: vue.get_title(course),
          });
        }
      });
      return new_list;
    },
    get_title(course_id) {
      var vue = this;
      var split_pos = course_id.lastIndexOf(" ");
      var dept_abr = course_id.substring(0, split_pos);
      var course_num = parseInt(
        course_id.substring(split_pos + 1, course_id.length)
      );
      var abbr_keys = Object.keys(this.graphData.x.nodes.department_abbrev);
      var num_keys = Object.keys(this.graphData.x.nodes.course_number);
      var title = "";

      abbr_keys.forEach(function (key) {
        if (vue.graphData.x.nodes.department_abbrev[key] === dept_abr) {
          num_keys.forEach(function (num_key) {
            if (vue.graphData.x.nodes.course_number[num_key] === course_num) {
              title = vue.graphData.x.nodes.course_title[num_key];
            }
          });
        }
      });
      return title;
    },
  },
};
</script>

<style lang="scss" scoped>
li {
  list-style-type: none;
  padding-bottom: 0.5rem;
}

.rounded-pill {
  font-size: 55%;
  vertical-align: middle;
}
</style>
