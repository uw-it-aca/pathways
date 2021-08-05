// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="row justify-content-center mb-5">
        <div class="col-md-9">
          <search-course :course-list="courseList"/>
        </div>
      </div>
      <div class="row">
          <div class="col-8"><course-details /></div>
          <div class="col-4"><explore-course /></div>
        </div>

      <div class="row">
        <div class="col">
          <grade-distribution />
        </div>
        <div class="col">
          <outcome-index />
        </div>
      </div>

      <prereq-map />

      <concurrent-courses />

      <contact-adviser-course />

    </template>
  </layout>
</template>

<script>
import courseList from '../data/courses.json';

import Layout from '../layout.vue';
import SearchCourse from '../components/search/course.vue';
import GradeDistribution from '../components/course/grade-distribution.vue';
import CourseDetails from '../components/course/course-details.vue';
import ExploreCourse from '../components/course/explore-course.vue'
import OutcomeIndex from '../components/course/outcome-index.vue';
import PrereqMap from '../components/course/prereq-map.vue';
import ConcurrentCourses from '../components/course/concurrent-courses.vue';
import ContactAdviserCourse from '../components/course/contact-adviser-course.vue';

export default {
  components: {
    'layout': Layout,
    'search-course': SearchCourse,
    'course-details': CourseDetails,
    'explore-course': ExploreCourse,
    'grade-distribution': GradeDistribution,
    'outcome-index': OutcomeIndex,
    'contact-adviser-course': ContactAdviserCourse,
    'prereq-map': PrereqMap,
    'concurrent-courses': ConcurrentCourses,
  },
  data() {
    return {
      pageTitle: 'Course',
      courseList,
    };
  },
  methods: {},
};
</script>

<style lang="scss" scoped>

</style>
