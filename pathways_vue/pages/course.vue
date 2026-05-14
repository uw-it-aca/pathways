// course.vue
<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <template v-if="courseData">
        <div class="row mt-5">
          <div class="col-md-4 col-12"><SearchMini /></div>
          <div class="order-md-first col-md-8 col-12">
            <h1 class="h2 ff-encode-sans fw-bold my-3 my-md-0" data-clarity-unmask="true">
              {{ courseData.course_id }}: {{ courseData.course_title }}
            </h1>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8 col-12">
            <CourseDetails :course="courseData" />
            <ExploreCourse :course="courseData" />
            <GradeDistribution :course="courseData" />
            <template v-if="courseCampus == 'seattle'">
              <OutcomeIndex :course="courseData" />
            </template>
            <!-- prereq map -->
            <PrereqMap
              :graph_data="courseData.prereq_graph"
              :active_course="courseId"
              :prereq_string="courseData.prereq_string"
            />
          </div>
          <div class="col-md-4 col-12">
            <ConcurrentCourses :courseData="courseData" />
            <ContactAdviser :campus="courseCampus" :type="'course'" />
          </div>
        </div>
      </template>
      <template v-else>
        <div class="row">
          <div v-if="showError" class="col col-md-9">
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
          <div v-else class="col col-md-9 text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </template>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import GradeDistribution from "@/components/course/grade-distribution.vue";
  import CourseDetails from "@/components/course/course-details.vue";
  import ExploreCourse from "@/components/course/explore-course.vue";
  import OutcomeIndex from "@/components/course/outcome-index.vue";
  import PrereqMap from "@/components/course/prereq-map.vue";
  import ConcurrentCourses from "@/components/course/concurrent-courses.vue";
  import ContactAdviser from "@/components/common/contact-adviser.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import utils from "@/utils.js";
  import { useCustomFetch } from "@/composables/customFetch";

  export default {
    name: "CourseComp",
    components: {
      DefaultLayout,
      CourseDetails,
      ExploreCourse,
      GradeDistribution,
      OutcomeIndex,
      ContactAdviser,
      PrereqMap,
      ConcurrentCourses,
      SearchMini
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
      async get_course_data(course_id) {
        const vue = this;
        this.courseData = undefined;

        try {
          const data = await useCustomFetch(
            "/api/v1/courses/details/" + course_id,
          );
          vue.showError = false;
          vue.courseData = data;
          vue.courseCampus = data.course_campus;
          vue.courseTitle = vue.courseId + ": " + data.course_title;
          vue.recentViewManager(
            vue.courseId,
            "course?id=" + vue.courseId,
            vue.courseCampus,
          );
        } catch (error) {
          vue.showError = true;
        }
      },
    },
    watch: {
      courseId(newValue) {
        this.get_course_data(newValue);
      },
    },
  };
</script>
