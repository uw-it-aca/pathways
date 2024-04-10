// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="d-flex flex-column">
        <div v-if="courseData" class="order-2 row justify-content-sm-center">
          <div class="col-md-9">
            <course-details :course="courseData" />
            <explore-course :course="courseData" />
          </div>

          <div class="col-md-9">
            <grade-distribution :course="courseData" />
          </div>
          <div v-if="courseCampus == 'seattle'" class="col-md-9">
            <outcome-index :course="courseData" />
          </div>
          <!-- prereq map -->
          <div class="col-md-9">
            <prereq-map
              :graph_data="courseData.prereq_graph"
              :active_course="courseId"
              :prereq_string="courseData.prereq_string"
            />
          </div>

          <div class="col-md-9">
            <concurrent-courses :courseData="courseData" />
          </div>
          <div class="col-md-9">
            <contact-adviser :campus="courseCampus" :type="'course'" />
          </div>
        </div>
        <div v-else class="row order-2 justify-content-sm-center">
          <div v-if="showError" class="col-md-9">
            <div class="alert alert-purple border-0" role="alert">
              <p>
                Data is not available for selected course. Here are some
                possible reasons:
              </p>
              <ul>
                <li>This course is no longer offered</li>
                <li>It is a graduate course</li>
                <li>You made a typo -- the course code doesn't exist.</li>
              </ul>
            </div>
          </div>
          <div v-else class="col-md-9 text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>

        <div class="order-1 row justify-content-center mb-5">
          <div class="col-md-9">
            <search-chooser
              :prefill-id="courseId"
              :prefill-campus="courseCampus"
              prefill-type="course"
              @update:selected="switch_course"
            />
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "@/layout.vue";
import SearchChooser from "@/components/search/chooser.vue";
import GradeDistribution from "@/components/course/grade-distribution.vue";
import CourseDetails from "@/components/course/course-details.vue";
import ExploreCourse from "@/components/course/explore-course.vue";
import OutcomeIndex from "@/components/course/outcome-index.vue";
import PrereqMap from "@/components/course/prereq-map.vue";
import ConcurrentCourses from "@/components/course/concurrent-courses.vue";
import ContactAdviser from "@/components/common/contact-adviser.vue";
import utils from "@/utils.js";

export default {
  name: "CourseComp",
  components: {
    layout: Layout,
    "search-chooser": SearchChooser,
    "course-details": CourseDetails,
    "explore-course": ExploreCourse,
    "grade-distribution": GradeDistribution,
    "outcome-index": OutcomeIndex,
    "contact-adviser": ContactAdviser,
    "prereq-map": PrereqMap,
    "concurrent-courses": ConcurrentCourses,
  },
  data() {
    return {
      courseData: undefined,
      courseId: undefined,
      courseTitle: undefined,
      courseCampus: undefined,
      showError: false,
      appName: "DawgPath",
    };
  },
  created() {
    this.recentViewManager = utils.recentViewManager;
  },
  computed: {
    pageTitle: function () {
      let no_title = this.showError ? "Error" : "Course";
      return this.courseTitle !== undefined
        ? (document.title = this.courseTitle + " - " + this.appName)
        : no_title;
    },
  },
  mounted() {
    this.courseId = this.$route.query.id;
    this.courseCampus = this.$route.query.campus;

    if (this.courseId == undefined) {
      this.showError = true;
    }

    this.emitter.on("update:selected", (selectedKey) => {
      this.courseId = selectedKey;
    });
  },
  methods: {
    switch_course(data) {
      this.courseId = data.id;
      this.courseCampus = data.campus;
    },
    get_course_data(course_id) {
      const vue = this;
      this.courseData = undefined;
      this.axios
        .get("/api/v1/courses/details/" + course_id)
        .then((response) => {
          vue.showError = false;
          vue.courseData = response.data;
          vue.courseCampus = response.data.course_campus;
          //vue.courseTitle = this.courseId + ': ' + response.data.course_title + ' - Course ';
          vue.courseTitle = this.courseId + ": " + response.data.course_title;
          vue.recentViewManager(vue.courseId, "course?id=" + vue.courseId, vue.courseCampus);
        })
        .catch(function () {
          vue.showError = true;
        });
    },
  },
  watch: {
    courseId(newValue) {
      this.get_course_data(newValue);
    },
  },
};
</script>
