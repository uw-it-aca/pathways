<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1 class="fs-2">{{ pageTitle }}</h1>
    </template>
    <template #content>
      <div class="mb-5 col-lg-8">
        <ul class="list-unstyled">
          <li><a href="#faq" class="text-decoration-none">Frequently Asked Questions</a></li>
          <li><a href="#terms" class="text-decoration-none">Term Definitions</a></li>
        </ul>

        <h2 class="fs-3" id="faq">Frequently Asked Questions</h2>
        <p>Remember to talk to an adviser when planning your course schedule.</p>
        <p>
          <span class="fw-bold">What is DawgPath?</span><br />
          It can be tough figuring out which courses to take. How do you find courses similar to
          ones you’ve really enjoyed? Of the courses you’ve already taken, which ones provide a
          foundation for more advanced coursework? What sequence of courses is best? DawgPath helps
          you discover interesting courses and enables you to be strategic about planning your
          course schedule.
        </p>
        <p>
          <span class="fw-bold">How often is the data updated?</span><br />
          The data is uploaded quarterly. When planning several quarters out, keep in mind that
          prerequisites may change over time.
        </p>
        <p>
          <span class="fw-bold">Why isn’t there data for all majors/courses?</span><br />
          In order to protect privacy, DawgPath only displays information for majors and courses if
          there are seven or more students.
        </p>
        <p>
          <span class="fw-bold">Does DawgPath include minors?</span><br />
          At this time DawgPath does not include data for minors.
        </p>
        <p>
          <span class="fw-bold">How is most commonly taken courses calculated?</span><br />
          Most commonly taken courses is a list of the most popular courses up to the point a
          student had declared their major.
        </p>
        <p>
          <span class="fw-bold"
            >How are double majors accounted for in data? What about when a student switches
            majors?</span
          ><br />
          Data is included for each major that a student declares.
        </p>
        <p>
          <span class="fw-bold">What is a histogram?</span><br />
          A histogram represents data in a range of buckets along the horizontal line, or x-axis.
          The vertical line, or y-axis, represents the number of outcomes for each bucket.
        </p>
        <p>
          <span class="fw-bold">Which instructors taught the course listed?</span><br />
          Course grade data is combined for all instructors who have taught the class.
        </p>
        <p>
          <span class="fw-bold">What is the course outcome index?</span><br />
          This index is calculated by estimating the number of PCs (pass/completion) for a course
          and subtracting the estimated PCs from the actual PCs to create an index rescaled to 0 to
          5. The index is calculated using the previous five years of course data.
        </p>
        <p>
          <span class="fw-bold">What does “average X00 level course” mean?</span><br />
          This is the average course outcome index for all X00 courses.
        </p>
        <p>
          <span class="fw-bold">What does “average course in XXX curriculum” mean?</span><br />
          This is the average course outcome index for all courses in a particular curriculum (e.g.
          CHEM/Chemistry)
        </p>
        <p>
          <span class="fw-bold"
            >Does Prereq Map consider specific requirements for majors and graduation?</span
          ><br />
          Prereq Map is based solely on course prerequisites and does not take into account specific
          requirements for majors or graduation. Majors typically have additional requirements
          beyond departmental course offerings.
        </p>
        <p>
          <span class="fw-bold">Are course equivalencies considered in the prereq map feature?</span
          ><br />
          Not all equivalencies (e.g. placement tests) are represented in the map – just UW courses.
          You can find some equivalencies in the text description.
        </p>

        <h2 class="fs-3" id="terms">Term Definitions</h2>
        <p>
          <span class="fw-bold">Declared major</span><br />
          A major is declared once the student has been accepted into the degree program and has
          officially declared the major.
        </p>

        <p><span class="fw-bold">Admission types:</span><br /></p>
        <p class="ms-4">
          <span class="fw-bold">Capacity-Constrained Admission</span><br />
          Capacity-constrained majors have additional requirements and selective screening, which
          may include an additional application process. Completing the minimum UW admission
          requirements does not guarantee admission to capacity-constrained majors.
        </p>

        <p class="ms-4">
          <span class="fw-bold">Open Admission</span><br />
          These majors are open to you when you’re admitted to the UW or anytime thereafter.
        </p>

        <p class="ms-4">
          <span class="fw-bold">Minimum Requirements/Selective Admission</span><br />
          These majors have additional admission requirements. Once you’re a UW student and meet the
          minimum requirements, you can be admitted without further screening.
        </p>

        <p class="ms-4">
          <span class="fw-bold">Cumulative grade point average</span><br />
          This is the average of the accumulated final grades earned in courses over time, weighted
          by the number of units per course.
        </p>
        <p>
          <span class="fw-bold">Cumulative grade point average</span><br />
          This is the average of the accumulated final grades earned in courses over time, weighted
          by the number of units per course.
        </p>
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
      pageTitle: 'DawgPath FAQ',
    };
  },
  methods: {},
};
</script>
