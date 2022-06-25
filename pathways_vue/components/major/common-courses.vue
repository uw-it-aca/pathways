//common-courses.

<template>
  <div class="card mb-5">
    <div v-if="commonCourses.length === 0" class="card-body">
      <h2 class="h4 pw-font-encode-sans">Common Courses</h2>
      <div class="alert alert-purple mt-2" role="alert">
        <p>
          No common courses available for
          <strong>{{ major["major_title"] }}</strong>.
        </p>
      </div>
    </div>
    <div v-else class="card-body explore-major">
      <h2 class="h4 pw-font-encode-sans">Common courses for {{ major["major_title"] }}</h2>
      <p>
        Below are the 10 most popular courses at the time of declaration among students who declared
        this major in the last 5 years.
      </p>

      <table class="table table-borderless table-striped">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" class="pe-0" style="width: 8%">
              Rank
            </th>
            <th scope="col" style="width: 92%">Common Course</th><!-- change this % to 62 when adding COI back in -->
            <th scope="col" class="px-0" style="width: 10%;min-width:60px;display:none;"><!-- hidden -->
              <abbr title="Course Outcome Index Score">COI </abbr>
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
          <tr v-for="course in commonCourses" class="align-middle">
            <th scope="row">
              <div class="icon-col">
                <icon-popover v-if="course.is_bottleneck" :variant="'bottleneck'" />
                <icon-popover v-if="course.is_gateway" :variant="'gateway'" />
              </div>
            </th>
            <td>
              <a
                v-bind:href="'/course?id=' + encodeURIComponent(course.course)"
                :title="'Go to course ' + course.course"
                class="btn-primary btn-course router-link-active text-decoration-none"
              >{{ course.course }}</a>
              <a
                v-bind:href="'/course?id=' + encodeURIComponent(course.course)"
                class="router-link-active ps-3"
                :title="'Go to course ' + course.course + ' ' + course.title"
              >{{ course.title }}</a>
            </td>
            <td v-if="course.coi_score" style="display:none;">{{ course.coi_score }}</td>
            <td v-else style="display:none;">No Data</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Popover } from 'bootstrap';
import IconPopover from '../common/icon-popover.vue';

export default {
  name: 'CommonCourses',
  components: {
    'icon-popover': IconPopover,
  },
  props: {
    major: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      commonCourses: []
    };
  },
  mounted() {
    this.commonCourses = this.get_common_courses();
    if (this.commonCourses.length > 0) {
      // var popover = new Popover(document.querySelector('.info-common-coi'));
      // var popover2 = new Popover(document.querySelector('.info-major-common'));
    }
  },
  methods: {
    get_common_courses: function () {
      let processed_courses = [];

      for (const [course, data] of Object.entries(this.major.common_course_decl)) {

        let style_string = `width: ${data['percent']}%`;
        processed_courses.push({
'course': course,
          'percent': data['percent'],
          'title': data['title'],
          'width': style_string,
          'coi_score': data['coi_score'],
          is_bottleneck: data['is_bottleneck'],
          is_gateway: data['is_gateway']
})
      }

      return processed_courses.sort((a, b) => (a.percent < b.percent) ? 1 : -1);
    }
  },
  watch: {
    commonCourses: function (course) {
      if (this.commonCourses.length > 0) {
        // Hack to get popovers to only init once element has rendered
        setTimeout(function () {
          var popover = new Popover(document.querySelector('.info-common-coi'));
        }, 1);

      }
    }
  }
};
</script>

<style lang="scss" scoped>
.table {
  --bs-table-striped-bg: rgba(179, 175, 124, 0.12);
}

tbody {
  counter-reset: rank;
}
tbody tr th:first-child::before {
  counter-increment: rank;
  content: counter(rank);
}

</style>
