// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="mb-5">
        <search-course />
      </div>

      <div class="mb-5">

        <h2>CHEM 162: General Chemistry</h2>
        <div><strong>Credits:</strong> 5</div>
        <div>
          <strong>Offered</strong>
          <ul class="ms-2 d-inline list-inline">
            <li class="list-inline-item"><span class="badge pw-green text-dark">SPR</span></li>
            <li class="list-inline-item"><span class="badge creamcicle text-dark">AUT</span></li>
            <li class="list-inline-item"><span class="badge bg-blue-200 text-dark">WIN</span></li>
          </ul>
        </div>

        <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Itaque numquam a maxime delectus tempora, ad molestiae rerum voluptate commodi cupiditate at quo fuga praesentium dicta repellendus quia et accusantium ab</p>
        <p><a href="#">View CHEM 162 course details and schedule on MyPlan</a></p>
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

      <contact-adviser />

    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import SearchCourse from '../components/search/course.vue';
import GradeDistribution from '../components/course/grade-distribution.vue';
import OutcomeIndex from '../components/course/outcome-index.vue';
import ContactAdviser from '../components/_common/contact-adviser.vue';
import PrereqMap from '../components/course/prereq-map.vue';
import ConcurrentCourses from '../components/course/concurrent-courses.vue';

export default {
  components: {
    'layout': Layout,
    'search-course': SearchCourse,
    'grade-distribution': GradeDistribution,
    'outcome-index': OutcomeIndex,
    'contact-adviser': ContactAdviser,
    'prereq-map': PrereqMap,
    'concurrent-courses': ConcurrentCourses,
  },
  data() {
    return {
      pageTitle: 'Course',
    };
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
@import "../css/custom.scss";

.creamcicle { background-color: $orange-200; }

</style>
