//common-courses.

<template>
  <div class="card mb-5">
    <div v-if="major.common_course_decl" class="card-body">
      <h3>Concurrent Courses</h3>
      <p>
        No common courses available for <strong>{{ major["major_title"] }}</strong>.
      </p>
    </div>
    <div v-else class="card-body explore-major">
      <h3>Common courses for {{ major["major_title"] }}</h3>
      <p>
        Below are the 10 most popular courses at the time of declaration among students who declared
        this major in the last 5 years.
      </p>

      <table class="table table-borderless table-striped">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" style="width: 5%">
              %
              <a
                tabindex="0"
                class="info-major-common"
                role="button"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
                data-bs-placement="top"
                title="Percentage"
                data-bs-content="Percent of students who had taken the course by the time they declared for major."
              >
                <i class="bi bi-info-circle-fill me-0"></i>
              </a>
            </th>
            <th scope="col" class="visually-hidden" style="width: 15%">Percentage Graph</th>
            <th scope="col" style="width: 50%">Common Course</th>
            <th scope="col" style="width: 30%">
              COI
              <a
                tabindex="0"
                class="info-common-coi"
                role="button"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
                data-bs-placement="top"
                title="Course Outcome Index"
                data-bs-content="A lower number (0-2) indicates that fewer people completed the course than predicted. A middle number (2-3) indicates the course is on target with predictions. A higher (3-5) number indicates that more people completed the course than anticipated."
              >
                <i class="bi bi-info-circle-fill me-0"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in common_courses" class="align-middle">
            <th scope="row">{{ course.percent }}%</th>
            <td>
              <div class="progress">
                <div
                  class="progress-bar bg-secondary"
                  role="progressbar"
                  :style="course.width"
                  :aria-valuenow="course.percent"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
            </td>
            <td>
              <a
                v-bind:href="'/course/?id=' + encodeURIComponent(course.course)"
                class="router-link-active"
              >
                <span class="badge bg-link-color text-light me-2">{{ course.course }}</span>
              </a>
              {{ course.title }}
            </td>
            <td v-if="course.coi_score">{{course.coi_score}}</td>
            <td v-else>No Data</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Popover } from 'bootstrap';

export default {
  name: 'CommonCourses',
  props: {
    major: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {};
  },
  mounted() {
    var popover = new Popover(document.querySelector('.info-common-coi'));
    var popover2 = new Popover(document.querySelector('.info-major-common'));
  },
  methods: {},
  computed: {
    common_courses: function () {
      let processed_courses = [];

      for (const [course, data] of Object.entries(this.major.common_course_decl)) {

        let style_string = `width: ${data['percent']}%`;
        processed_courses.push({'course': course,
          'percent': data['percent'],
          'title': data['title'],
          'width': style_string,
          'coi_score': data['coi_score']})
      }

      return processed_courses.sort((a, b) => (a.percent < b.percent) ? 1 : -1);
    }
  }
};
</script>

<style lang="scss" scoped>
.table {
  --bs-table-striped-bg: rgba(179, 175, 124, 0.12);
}
</style>
