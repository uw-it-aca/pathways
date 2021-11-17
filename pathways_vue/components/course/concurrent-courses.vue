// concurrent-courses.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h3>Concurrent Courses</h3>
      <p>
        Students who took <strong>{{courseData.course_id}}</strong> in the past 2 years also took the following
        courses at the same time.
      </p>
      <table class="table table-borderless">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" style="width: 10%">
              %
              <a
                tabindex="0"
                class="info-course-concurrent"
                role="button"
                data-bs-toggle="popover"
                data-bs-trigger="focus"
                title="Percentage"
                data-bs-content="Description needed."
              >
                <i class="bi bi-info-circle-fill"></i>
              </a>
            </th>
            <th scope="col" class="visually-hidden" style="width: 30%">Percentage Graph</th>
            <th scope="col" style="width: 30%">Concurrent Course</th>
            <th scope="col" style="width: 30%">COI</th>
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
              <a href="/course/?code=CSS+415" class="router-link-active"
                ><span class="badge bg-link-color text-light">{{course.course}}</span></a
              >
              {{course.title}}
            </td>
            <td>{{course.coi_score}}</td>
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
    var popover = new Popover(document.querySelector('.info-course-concurrent'));
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

<style lang="scss"></style>
