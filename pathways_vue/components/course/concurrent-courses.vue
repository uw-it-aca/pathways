// concurrent-courses.vue

<template>
  <div class="card mb-5">
    <div v-if="concurrent_courses.length === 0" class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Concurrent Courses</h2>
      <div class="alert alert-purple" role="alert">
        <p>
          No concurrent courses available for
          <strong>{{ courseData.course_id }}</strong
          >.
        </p>
      </div>
    </div>
    <div v-else class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Concurrent Courses</h2>
      <p>
        Students who took <strong>{{ courseData.course_id }}</strong> in the
        past 2 years also took the following courses at the same time.
      </p>
      <table class="table table-borderless table-striped">
        <thead>
          <tr class="bg-light text-dark">
            <th scope="col" class="pe-0" style="width: 5%"></th>
            <th scope="col" class="pe-0" style="width: 5%">
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
            <!-- <th scope="col" class="visually-hidden" style="width: 20%">Percentage Graph</th> -->
            <th scope="col" style="width: 90%">Concurrent Course</th>
            <!-- change this % to 62 when adding COI back in -->
            <th
              scope="col"
              class="px-0"
              style="width: 10%; min-width: 60px; display: none"
            >
              <!-- hidden -->
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
          <tr
            class="align-middle"
            v-for="(course, index) in concurrent_courses"
            :key="index"
          >
            <th scope="row">
              <div class="icon-col">
                <icon-popover
                  v-if="course.is_bottleneck"
                  :variant="'bottleneck'"
                />
                <icon-popover v-if="course.is_gateway" :variant="'gateway'" />
              </div>
            </th>
            <td>{{ course.percent }}%</td>
            <!-- <td>
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
            </td> -->
            <td>
              <a
                :href="'/course?id=' + course.course"
                :title="'Go to course ' + course.course"
                class="btn-primary btn-course router-link-active text-decoration-none"
                >{{ course.course }}</a
              >
              <a
                :href="'/course?id=' + course.course"
                class="router-link-active ps-3"
                :title="'Go to course ' + course.course + ' ' + course.title"
              >
                {{ course.title }}</a
              >
            </td>
            <td v-if="course.coi_score" style="display: none">
              {{ course.coi_score }}
            </td>
            <!-- hidden -->
            <td v-else style="display: none">No Data</td>
            <!-- hidden -->
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Popover } from "bootstrap";
import IconPopover from "../common/icon-popover.vue";

export default {
  name: "ConcurrentCourses",
  components: {
    "icon-popover": IconPopover,
  },
  props: {
    courseData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  mounted() {
    if (this.concurrent_courses.length > 0) {
      var popover = new Popover(
        document.querySelector(".info-course-concurrent")
      );
      //var popover = new Popover(document.querySelector('.info-common-coi'));
    }
  },
  methods: {},
  computed: {
    concurrent_courses: function () {
      if (!this.courseData.concurrent_courses) {
        return [];
      }
      let processed_courses = [];
      for (const [course, data] of Object.entries(
        this.courseData.concurrent_courses
      )) {
        let percent = Math.round(data["percent"] * 100);
        let style_string = `width: ${percent}%`;

        processed_courses.push({
          course: course,
          percent: percent,
          title: data["title"],
          width: style_string,
          coi_score: data["coi_score"],
          is_bottleneck: data["is_bottleneck"],
          is_gateway: data["is_gateway"],
        });
      }
      return processed_courses
        .sort((a, b) => (a.percent < b.percent ? 1 : -1))
        .slice(0, 10);
    },
  },
};
</script>

<style lang="scss">
.table {
  --bs-table-striped-bg: rgb(179 175 124 / 12%);
}

.icon-col {
  .round-sm {
    height: 18px;
    width: 18px;
    line-height: 18px;
    border-radius: 15px;
    font-size: 0.7em;

    .material-symbols-outlined {
      font-size: 0.8rem;
    }
  }
}
</style>
