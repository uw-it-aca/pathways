// prereq-curr-list.

<template>
  <p class="fw-bold">
    NOTE: This is an overview of every course in the department. For information
    on majors, please search for a major using the main search function. Some
    courses may require multiple prerequisites before completion.
  </p>
  <ul class="list-unstyled">
    <li v-for="(course, index) in courseData" :key="index" class="mb-3">
      <div class="card shadow-sm">
        <div class="card-body p-3">
          <h3 class="fs-6 d-flex justify-content-between">
            <a
              :href="'/course?id=' + course.course_id"
              class="d-inline-block mb-3"
              :title="
                'Go to course ' + course.course_id + ' ' + course.course_title
              "
            >
              {{ course.course_id }}: {{ course.course_title }}</a
            >
            <button
              type="button"
              class="btn btn-outline-secondary btn-sm"
              data-bs-toggle="collapse"
              :data-bs-target="'#collapsePrereqs_' + index"
              aria-expanded="false"
              aria-controls="collapsePrereqs"
            >
              Show/hide list
            </button>
          </h3>
          <div :id="'collapsePrereqs_' + index" class="collapse">
            <div class="container">
              <div class="row">
                <div class="p-0 mb-3 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Prerequisites</strong>
                      <span class="badge rounded-pill bg-purple">{{
                        course.prereqs.length
                      }}</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <ul v-if="course.prereqs.length > 0" class="prereq-list">
                    <li
                      v-for="(prereq, index2) in course.prereqs"
                      :key="index2"
                    >
                      <a
                        :href="'/course?id=' + prereq.course_id"
                        class="btn-primary btn-course router-link-active text-decoration-none"
                      >
                        {{ prereq.course_id }}</a
                      >
                    </li>
                  </ul>

                  <div v-else>
                    <small>This course has no prerequisites.</small>
                  </div>
                </div>
                <div class="p-0 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Is a prerequisite for</strong>
                      <span class="badge rounded-pill bg-purple">{{
                        course.postreqs.length
                      }}</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <ul v-if="course.postreqs.length > 0" class="prereq-list">
                    <li
                      v-for="(postreq, index3) in course.postreqs"
                      :key="index3"
                    >
                      <a
                        :href="'/course?id=' + postreq.course_id"
                        class="btn-primary btn-course router-link-active text-decoration-none"
                      >
                        {{ postreq.course_id }}</a
                      >
                    </li>
                  </ul>
                  <div v-else>
                    <small
                      >This course is not a prerequisite for other
                      courses.</small
                    >
                  </div>
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
  name: "PrereqCurrList",
  props: {
    courseData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {};
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
  content: "";
}

.rounded-pill {
  font-size: 75%;
  margin-left: 0.3rem;
}
</style>
