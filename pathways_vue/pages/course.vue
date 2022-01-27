// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>
    <template #content>
      <div class="row justify-content-center mb-5">
        <div class="col-md-9">
          <search-chooser
            :prefill-id="courseId"
            :prefill-campus="courseCampus"
            prefill-type="course"
            @update:selected="switch_course"
          />
        </div>
      </div>

      <div v-if="courseData">
        <div class="row justify-content-sm-center">
          <div class="col-md-9">
            <div class="row">
              <div class="col-sm-8">
                <course-details :course="courseData" />
              </div>
              <div class="col-sm-4">
                <explore-course :course="courseData" />
              </div>
            </div>
          </div>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-9">
            <div class="row">
              <div class="col-sm-8"> <!-- change this class to col-sm-6 when adding COI graph -->
                <grade-distribution :course="courseData" />
              </div>
         <!-- <div class="col-sm-6">
                <outcome-index :course="courseData"/>
              </div>-->
            </div>
          </div>
        </div>
        <!-- prereq map -->
        <div class="row justify-content-center">
          <div class="col-md-9">
            <prereq-map :graph_data="courseData.prereq_graph" :active_course="courseId" />
          </div>
        </div>

        <div class="row justify-content-center">
          <div class="col-md-9">
            <concurrent-courses :courseData="courseData" />
          </div>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-9">
            <contact-adviser :campus="courseCampus" :type="'course'" />
          </div>
        </div>
      </div>
      <div v-else>
        <div v-if="showError">
          <div class="alert alert-purple" role="alert">
            <p>Data is not available for selected course. Here are some possible reasons:</p>
            <ul>
              <li>This course is no longer offered</li>
              <li>It is a graduate course</li>
              <li>You made a typo -- the course code doesn’t exist.</li>
            </ul>
          </div>
        </div>
        <div v-else>
          <div class="d-flex justify-content-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import SearchChooser from "../components/search/chooser.vue";
import GradeDistribution from '../components/course/grade-distribution.vue';
import CourseDetails from '../components/course/course-details.vue';
import ExploreCourse from '../components/course/explore-course.vue';
import OutcomeIndex from '../components/course/outcome-index.vue';
import PrereqMap from '../components/course/prereq-map.vue';
import ConcurrentCourses from '../components/course/concurrent-courses.vue';
import ContactAdviser from '../components/common/contact-adviser.vue';

export default {
  components: {
    layout: Layout,
    'search-chooser': SearchChooser,
    'course-details': CourseDetails,
    'explore-course': ExploreCourse,
    'grade-distribution': GradeDistribution,
    'outcome-index': OutcomeIndex,
    'contact-adviser': ContactAdviser,
    'prereq-map': PrereqMap,
    'concurrent-courses': ConcurrentCourses,
  },
  data() {
    return {
      courseData: undefined,
      courseId: undefined,
      courseTitle: undefined,
      courseCampus: undefined,
      showError: false
    };
  },
  computed: {
    pageTitle: function () {
      let no_title = this.showError ? "Error" : "";
      return this.courseTitle !== undefined ? this.courseTitle : no_title;
    }
  },
  mounted() {
    let course_id = this.$route.query.id;
    this.courseId = course_id;
    this.courseCampus = this.$route.query.campus;
    this.emitter.on("update:selected", selectedKey => {
      this.courseId = selectedKey;

    })
  },
  methods: {
    switch_course(data) {
      this.courseId = data.id;
      this.courseCampus = data.campus
    },
    get_course_data(course_id) {
      const vue = this;
      this.courseData = undefined;
      this.axios.get("/api/v1/courses/details/" + course_id).then((response) => {
        vue.showError = false;
        vue.courseData = response.data;
        vue.courseCampus = response.data.course_campus;
        vue.courseTitle = this.courseId + ": " + response.data.course_title + " - Course ";
      }).catch(function (error) {
        vue.showError = true;
      });
    }
  },
  watch: {
    courseId(newValue) {
      this.get_course_data(newValue);
    }
  }
};
</script>

<style lang="scss" scoped></style>
