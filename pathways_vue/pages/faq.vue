<template>
  <layout :page-title="pageTitle">
    <template #title>
      <h1 class="fs-2">{{ pageTitle }}</h1>
    </template>
    <template #content>
      <div class="card mb-5 col-lg-8">
        <div class="card-body">
          <ul class="list-unstyled">
            <li>
              <a href="#dawgpath" class="text-decoration-none">What is DawgPath?</a>
            </li>
            <li>
              <a href="#howdp" class="text-decoration-none">How does DawgPath do this?</a>
            </li>
            <li>
              <a href="#data_update" class="text-decoration-none">How often is the data updated?</a>
            </li>
            <li>
              <a
                href="#data_privacy"
                class="text-decoration-none"
              >Why isn’t there data for all majors/courses?</a>
            </li>
            <li>
              <a href="#minors" class="text-decoration-none">Does DawgPath include minors?</a>
            </li>
            <li>
              <a
                href="#common_courses"
                class="text-decoration-none"
              >How is most commonly taken courses calculated?</a>
            </li>
            <li>
              <a href="#double_majors" class="text-decoration-none">
                How are double majors accounted for in data? What about when a student switches
                majors?
              </a>
            </li>
            <li>
              <a href="#histogram" class="text-decoration-none">What is a histogram?</a>
            </li>
            <li>
              <a
                href="#instructors"
                class="text-decoration-none"
              >Which instructors taught the course listed?</a>
            </li>
            <!-- <li>
              <a href="#coi" class="text-decoration-none">What is the course outcome index?</a>
            </li>
            <li>
              <a
                href="#coi_level_course"
                class="text-decoration-none"
              >What does “average X00 level course” mean?</a>
            </li>
            <li>
              <a
                href="#coi_curriculum"
                class="text-decoration-none"
              >What does “average course in XXX curriculum” mean?</a>
            </li>-->
            <li>
              <a
                href="#pm_reqs"
                class="text-decoration-none"
              >Does Prereq Map consider specific requirements for majors and graduation?</a>
            </li>
            <li>
              <a
                href="#pm_equivalencies"
                class="text-decoration-none"
              >Are course equivalencies considered in the prereq map feature?</a>
            </li>
            <li class="mt-3">
              <a href="#terms" class="text-decoration-none mt-3">Term Definitions</a>
            </li>
            <li>
              <a href="#declared_major" class="text-decoration-none ms-4">Declared Major</a>
            </li>
            <li>
              <a href="#cgpa" class="text-decoration-none ms-4">Cumulative Grade Point Average</a>
            </li>
            <li class="mt-3">
              <a href="#admission_types" class="text-decoration-none">Admission Types</a>
            </li>
            <li>
              <a
                href="#capacity_constrained"
                class="text-decoration-none ms-4"
              >Capacity-Constrained Admission</a>
            </li>
            <li>
              <a href="#open_admission" class="text-decoration-none ms-4">Open Admission</a>
            </li>
            <li>
              <a href="#minimum_reqs" class="text-decoration-none ms-4">Minimum Requirements</a>
            </li>
            <li>
              <a href="#mixed" class="text-decoration-none ms-4">Mixed Admission</a>
            </li>
          </ul>

          <p><em>Remember to talk to an adviser when planning your course schedule.</em></p>
          
          <h2 class="fs-3 visually-hidden" id="questions">Questions</h2>
          <h3 id="dawgpath" class="fw-bold fs-5">What is DawgPath?</h3>
          <p>
            DawgPath helps you discover interesting courses and majors and enables you to be strategic about planning your course schedule. It can be tough figuring out which courses to take and what to major in. How do you find courses similar to ones you’ve really enjoyed? Of the courses you’ve already taken, how do you learn which ones provide a foundation for more advanced coursework? How do you know which courses to take when, and what sequence of courses is most likely to set you up for success? DawgPath helps you answer these questions to create a path that works for you.
          </p>
          <h3 id="howdp" class="fw-bold fs-5">How does DawgPath do this?</h3>
          <p>
            Leveraging data from UW’s databases, DawgPath provides two views to help students manage and navigate: Course View and Major View. 
          </p>
          <p>
            DawgPath Course View:
            <ul>
              <li>Visualizes grading patterns for every UW course across the three campuses</li>
              <li>Lists courses that are often taken concurrently</li>
              <li>Displays the prerequisites for a course and the courses that can be taken upon completion of the course</li>
              <!-- <li>Provides an index that measures the grade outcomes for each course</li> -->
              <li>Makes it easy to connect with an adviser</li>
              <li>Enables users to search for courses by topic (e.g., social justice)</li>
            </ul>
            DawgPath Major View:
            <ul>
              <li>Displays the distribution of cumulative GPAs of students who were accepted to a capacity-constrained major</li>
              <li>A list of commonly taken courses among students who declared the major</li>
              <li>Enables users to search for majors by topic (e.g., Ecology)</li>
            </ul>
          </p>

          <h3 id="data_update" class="fw-bold fs-5">How often is the data updated?</h3>
          <p>
            All of the data is updated quarterly. When planning several quarters out, keep in mind that prerequisites may change over time.
          </p>

          <h3 id="data_privacy" class="fw-bold fs-5">Why isn’t there data for all majors/courses?</h3>
          <p>
            In order to protect privacy, DawgPath displays information only for majors and courses that have seven or more students.
          </p>

          <h3 id="minors" class="fw-bold fs-5">Does DawgPath include minors?</h3>
          <p>At this time DawgPath does not include data for minors.</p>

          <h3
            id="common_courses"
            class="fw-bold fs-5"
          >How is the data most commonly taken courses calculated?</h3>
          <p>
            Most commonly taken courses is a list of the most popular courses up to the point a student had declared their major. 
          </p>

          <h3 id="double_majors" class="fw-bold fs-5">
            How are double majors accounted for in data? What about when a student switches
            majors?
          </h3>
          <p>Data is included for each major that a student declares.</p>

          <h3 id="histogram" class="fw-bold fs-5">What is a histogram?</h3>
          <p>
            A histogram represents data in a range of containers along the horizontal line, or x-axis. The vertical line, or y-axis, represents the number of outcomes for each container.
          </p>

          <h3 id="instructors" class="fw-bold fs-5">Which instructors taught the course listed?</h3>
          <p>All of the instructors who have taught the class within the chosen timeframe are included and the results are aggregated. </p>

          <!-- <h3 id="coi" class="fw-bold fs-5">What is the course outcome index?</h3>
          <p>
            This index is calculated by estimating the number of PCs (pass/completion) for a course and subtracting the estimated PCs from the actual PCs to create an index rescaled to -5 to 5. The index is calculated using the previous five years of course data.
          </p>

          <h3 id="coi_level_course" class="fw-bold fs-5">What does “average X00 level course” mean?</h3>
          <p>This is the average course outcome index for all X00 courses. For example, the average COI for all 100 level courses would include Biology 140, Chem 142 and all other 100-level courses.</p>

          <h3
            id="coi_curriculum"
            class="fw-bold fs-5"
          >What does “average course in XXX curriculum” mean?</h3>
          <p>
            This is the average course outcome index for all courses in a particular curriculum (e.g. CHEM/Chemistry).
          </p> -->

          <h3
            id="pm_reqs"
            class="fw-bold fs-5"
          >Does Prereq Map consider specific requirements for majors and graduation?</h3>
          <p>
            Prereq Map is based solely on course prerequisites and does not take into account specific requirements for majors or graduation. Majors typically have additional requirements beyond departmental course offerings.
          </p>

          <h3
            id="pm_equivalencies"
            class="fw-bold fs-5"
          >Are course equivalencies considered in the Prereq Map feature?</h3>
          <p>
            Not all equivalencies (e.g. placement tests) are represented in the map – just UW courses. You can find some equivalencies in the text description.
          </p>

          <h2 class="fs-3 mt-4" id="terms">Term Definitions</h2>

          <h3 id="declared_major" class="fw-bold fs-5">Declared major</h3>
          <p>
            A major is declared for selective screening majors once a student has been accepted into a degree program and has officially declared the major.
          </p>

          <h3 id="cgpa" class="fw-bold fs-5">Cumulative grade point average</h3>
          <p>
            The average of the accumulated final grades earned in courses over time, weighted by the number of units per course.
          </p>

          <h2 id="admission_types" class="fs-3 mt-4">Admission Types</h2>

          <h3 id="capacity_constrained" class="fw-bold fs-5">Capacity-Constrained Admission</h3>
          <p>
            Capacity-constrained majors have additional requirements and selective screening, which may include an additional application process. Completing the minimum UW admission requirements does not guarantee admission to capacity-constrained majors.
          </p>

          <h3 id="open_admission" class="fw-bold fs-5">Open Admission</h3>
          <p>Open Admission majors are open to any student when admitted to the UW or anytime thereafter.</p>

          <h3 id="minimum_reqs" class="fw-bold fs-5">Minimum Requirements/Selective Admission</h3>
          <p>
            These majors have additional admission requirements. Once a UW student meets the minimum requirements, they can be admitted without further screening.
          </p>
          <h3 id="mixed" class="fw-bold fs-5">Mixed Admission</h3>
          <p>Entry may be either open, minimum, or capacity-constrained depending on the degree/option chosen.</p>
        </div>
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
      pageTitle: 'Frequently Asked Questions',
    };
  },
  methods: {},
};
</script>
