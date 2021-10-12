<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1 class="fs-2">{{ pageTitle }}</h1>
    </template>
    <template #content>
      <div class="mb-5">
        <ul class="list-unstyled">
          <li><a href="#faq" class="text-decoration-none">Frequently Asked Questions</a></li>
          <li><a href="#gpa" class="text-decoration-none m-4">Declared major cumulative GPA distribution</a></li>
          <li><a href="#cgd" class="text-decoration-none m-4">Course grade distribution</a></li>
          <li><a href="#coi" class="text-decoration-none m-4">Course outcome index</a></li>
          <li><a href="#pm" class="text-decoration-none m-4">Prerequisite Map</a></li>
          <li><a href="#terms" class="text-decoration-none">Term Definitions</a></li>
        </ul>

        <h2 class="fs-3" id="faq">Frequently Asked Questions</h2>
        <p>
          <span class="fw-bold">What is DawgPath?</span><br />
          It can be tough figuring out which courses to take. How do you find courses similar to
          ones you’ve really enjoyed? Of the courses you’ve already taken, which ones provide a
          foundation for more advanced coursework? What sequence of courses is best? DawgPath helps
          you discover interesting courses and enables you to be strategic about planning your course
          schedule.
        </p>

        <h3 class="fs-5 about ms-4" id="gpa">Declared major cumulative GPA distribution</h3>
        <p class="ms-4">
          <span class="fw-bold">Q: </span><br />
          A:
        </p>

        <h3 class="fs-5 about ms-4" id="cgd">Course grade distribution</h3>
        <p class="ms-4">
          <span class="fw-bold">Q: </span><br />
          A:
        </p>

        <h3 class="fs-5 about ms-4" id="coi">Course outcome index</h3>
        <p class="ms-4">
          <span class="fw-bold">Q: </span><br />
          A:
        </p>

        <h3 class="fs-5 about ms-4" id="pm">Prerequisite Map</h3>
      <p class="ms-4">
          <span class="fw-bold">Q: </span><br />
          A:
        </p>

        <h2 class="fs-3" id="terms">Term Definitions</h2>
        <span class="fw-bold">Q</span><br />
          A
        </div>
    </template>
  </layout>
</template>

<style lang="scss">

  .fs-5.about {
    color: #452a78;
    font-weight: bold;
  }

</style>

<script>
import Layout from '../layout.vue';

export default {
  name: 'App',
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'FAQ & Term Definitions',
    };
  },
  methods: {},
};
</script>
