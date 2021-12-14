// prereq-curr-list.

<template>
  <p class="fw-bold">
    NOTE: This is an overview of every course in the department. For information on majors,
    please search for a major using the main search function.
  </p>
  <ul class="list-unstyled">
    <li class="mb-3" v-for="course in courseData">
      <div class="card shadow-sm">
        <div class="card-body p-3">
          <strong
            ><a :href="'/course/?id=' + course.course_id" class="d-block mb-3">
              {{course.course_id}}: {{course.course_title}}</a
            ></strong
          >
          <div>
            <div class="container">
              <div class="row">
                <div class="p-0 mb-3 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Prerequisites</strong>
                      <span class="badge rounded-pill bg-purple">{{course.prereqs.length}}</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <ul class="prereq-list" v-if="course.prereqs.length > 0">
                    <li v-for="prereq in course.prereqs">
                      <a :href="'/course/?id=' + prereq.course_id" class="active-router-link"><span class="badge bg-link-color text-light"
                        >{{prereq.course_id}}</span></a
                      >
                    </li>
                  </ul>

                  <div v-else><small>This course has no prerequisites.</small></div>
                </div>
                <div class="p-0 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Available upon completion</strong>
                      <span class="badge rounded-pill bg-purple">{{course.postreqs.length}}</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <ul class="prereq-list" v-if="course.postreqs.length > 0">
                    <li v-for="postreq in course.postreqs">
                      <a :href="'/course/?id=' + postreq.course_id" class="active-router-link"><span class="badge bg-link-color text-light"
                      >{{postreq.course_id}}</span></a
                      >
                    </li>
                  </ul>
                  <div v-else><small>No courses made available.</small></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'PrereqCurrList',
  data() {
    return {};
  },
  props: {
    courseData: {
      type: Array,
      required: true,
    }
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.prereq-list {
  list-style: none;
  padding: 0;
}

.prereq-list li {
  display: inline-block;
  margin-right: 5px;
}

.prereq-list li:last-child a::after {
  content: '';
}

.rounded-pill {
  font-size: 75%;
  margin-left: 0.3rem;
}
</style>
