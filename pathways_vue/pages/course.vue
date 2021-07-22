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
            <li class="list-inline-item"><span class="badge bg-danger text-dark">Info</span></li>
            <li class="list-inline-item"><span class="badge bg-info text-dark">Info</span></li>
            <li class="list-inline-item"><span class="badge bg-success text-dark">Info</span></li>
          </ul>
        </div>

        <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Itaque numquam a maxime delectus tempora, ad molestiae rerum voluptate commodi cupiditate at quo fuga praesentium dicta repellendus quia et accusantium ab</p>
        <p><a href="#">View CHEM 162 course details and schedule on MyPlan</a></p>
      </div>

      <grade-distribution />
      <difficulty-index />

      <div class="card mb-5">
        <div class="card-body">Prerequisite Map</div>
      </div>

      <div class="card mb-5">
        <div class="card-body">Concurrent Courses</div>
      </div>

      <contact-adviser />

      <d3-arc />

    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import SearchCourse from '../components/search/course.vue';
import GradeDistribution from '../components/course/grade-distribution.vue';
import DifficultyIndex from '../components/course/difficulty-index.vue';
import ContactAdviser from '../components/_common/contact-adviser.vue';
import D3Arc from '../components/d3-arc.vue';

export default {
  components: {
    'layout': Layout,
    'search-course': SearchCourse,
    'grade-distribution': GradeDistribution,
    'difficulty-index': DifficultyIndex,
    'contact-adviser': ContactAdviser,
    'd3-arc': D3Arc,
  },
  data() {
    return {
      pageTitle: 'Course',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
