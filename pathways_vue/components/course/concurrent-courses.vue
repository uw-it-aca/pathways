// concurrent-courses.vue

<template>
  <div class="card mb-5">
    <div v-if="concurrent_courses.length === 0" class="card-body">
      <h3>Concurrent Courses</h3>
      <p>
        No concurrent courses available for <strong>{{courseData.course_id}}</strong>.
      </p>
    </div>
    <div v-else class="card-body">
      <h3>Concurrent Courses</h3>
      <p>
        Students who took <strong>{{courseData.course_id}}</strong> in the past 2 years also took the following
        courses at the same time.
      </p>
      <table class="table table-borderless table-striped">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" style="width: 5%">
              %
              <a
                tabindex="0"
                class="info-course-concurrent"
                role="button"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
                data-bs-placement="top"
                title="Concurrent Courses"
                data-bs-content="Percentage of students who took the two courses at the same time."
              >
                <i class="bi bi-info-circle-fill me-0"></i>
              </a>
            </th>
            <th scope="col" class="visually-hidden" style="width: 15%">Percentage Graph</th>
            <th scope="col" style="width: 50%">Concurrent Course</th>
            <th scope="col" style="width: 30%">COI
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
          <tr class="align-middle" v-for="course in concurrent_courses">
            <th scope="row">{{course.percent}}%</th>
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
              <a :href="'/course/?id=' + course.course" class="btn-primary btn-course router-link-active text-decoration-none"
                >{{course.course}}</a
              >
              {{course.title}}
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
  name: 'ConcurrentCourses',
    props: {
    courseData: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {};
  },
  mounted() {
    if(this.concurrent_courses.length > 0){
      var popover = new Popover(document.querySelector('.info-course-concurrent'));
      var popover = new Popover(document.querySelector('.info-common-coi'));
    }
  },
  methods: {},
  computed: {
    concurrent_courses: function (){
      if(!this.courseData.concurrent_courses){
        return []
      }
      let processed_courses = [];
      for (const [course, data] of Object.entries(this.courseData.concurrent_courses)) {
        let percent = Math.round(data['percent'] * 100)
        let style_string = `width: ${percent}%`;

        processed_courses.push({'course': course,
                                 'percent': percent,
                                 'title': data['title'],
                                 'width': style_string,
                                 'coi_score': data['coi_score']})
      }
      return processed_courses.sort((a, b) => (a.percent < b.percent)? 1 : -1).slice(0, 10);
    }
  }
};
</script>

<style lang="scss">
@import '../../css/custom.scss';
.table {
  --bs-table-striped-bg: rgba(179, 175, 124, 0.12);
}
</style>
