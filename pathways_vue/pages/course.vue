// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="mb-5">
        <h2>CHEM 162: General Chemistry</h2>
        <div>Credits: 5</div>
        <div>Offered <span class="badge bg-info text-dark">Info</span> <span class="badge bg-info text-dark">Info</span></div>
        <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Itaque numquam a maxime delectus tempora, ad molestiae rerum voluptate commodi cupiditate at quo fuga praesentium dicta repellendus quia et accusantium ab</p>
        <p><a href="#">View CHEM 162 course details and schedule on MyPlan</a></p>
      </div>

      <grade-distribution />

      <div class="card mb-5">
        <div class="card-body">Course Difficulty Index (CDI)</div>
      </div>

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
import GradeDistribution from '../components/course/grade-distribution.vue';
import ContactAdviser from '../components/course/contact-adviser.vue';
import D3Arc from '../components/d3-arc.vue';

export default {
  components: {
    layout: Layout,
    'grade-distribution': GradeDistribution,
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
