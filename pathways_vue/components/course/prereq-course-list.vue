//prereq-course-list.vue

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h4>Prerequesites <span class="badge rounded-pill bg-purple">{{prereqs.length}}</span></h4>
      <div class="mt-3">
        <ul class="list-unstyled mb-0">
          <li v-for="prereq in prereqs">
            <a :href="'/course/?code='+prereq.course_id" class="router-link-active">
              <span class="badge bg-link-color text-light">{{prereq.course_id}}</span>
            </a>
            <span class="ms-3">{{prereq.course_title}}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="card mb-3">
    <div class="card-body">
      <h4>
        Courses Available Upon Completion <span class="badge rounded-pill bg-purple">{{postreqs.length}}</span>
      </h4>
      <div class="mt-3">
        <ul class="list-unstyled mb-0">
          <li v-for="postreq in postreqs">
            <a :href="'/course/?code='+postreq.course_id" class="router-link-active">
              <span class="badge bg-link-color text-light">{{postreq.course_id}}</span>
            </a>
            <span class="ms-3">{{postreq.course_title}}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrereqCourseList',
  data() {
    return {
      prereqs: [],
      postreqs: []
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
  mounted() {
    this.build();
  },
  computed: {
    course_url: function (){
    }
  },
  methods: {
    build: function(){
      this.prereqs = this.get_courses_from_list(this.active_course, this.graph_data.x.edges.from);
      this.postreqs = this.get_courses_from_list(this.active_course, this.graph_data.x.edges.to);
    },
    get_courses_from_list(current_course, list) {
      var values = [...new Set(Object.values(list))];
      var vue = this;
      var new_list = [];
      values.forEach(function(course) {
        if (current_course !== course && !new_list.includes(course)) {
          new_list.push({
            "course_id": course,
            "course_title": vue.get_title(course)
          });
        }
      });
      return new_list;
    },
    get_title(course_id){
      var vue = this;
      var split_pos = course_id.lastIndexOf(" ");
      var dept_abr = course_id.substring(0, split_pos);
      var course_num = parseInt(course_id.substring(split_pos + 1, course_id.length));
      var abbr_keys = Object.keys(this.graph_data.x.nodes.department_abbrev);
      var num_keys = Object.keys(this.graph_data.x.nodes.course_number);
      var title = "";

      abbr_keys.forEach(function(key){
        if(vue.graph_data.x.nodes.department_abbrev[key] === dept_abr){
          num_keys.forEach(function(num_key){
            if(vue.graph_data.x.nodes.course_number[num_key] === course_num){
               title = vue.graph_data.x.nodes.course_title[num_key];
            }
          });
        }
      });
      return title;
    }
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
