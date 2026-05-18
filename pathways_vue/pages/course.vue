<template>
  <DefaultLayout :page-title="pageTitle">
    <template #content>
      <template v-if="courseData">
        <div class="row mt-5">
          <div class="col-md-4 col-12"><SearchMini /></div>
          <div class="order-md-first col-md-8 col-12">
            <h1
              class="h2 ff-encode-sans fw-bold my-md-0 my-3"
              data-clarity-unmask="true"
            >
              {{ courseData.course_id }}: {{ courseData.course_title }}
            </h1>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8 col-12">
            <CourseDetails :course="courseData" />
            <ExploreCourse :course="courseData" />
            <GradeDistribution :course="courseData" />
            <OutcomeIndex
              v-if="courseCampus === 'seattle'"
              :course="courseData"
            />
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
          <div v-else-if="loading" class="col col-md-9 text-center">
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
  import { defineAsyncComponent } from "vue";
  import DefaultLayout from "@/layouts/default.vue";
  import CourseDetails from "@/components/course/course-details.vue";
  import ExploreCourse from "@/components/course/explore-course.vue";
  import ContactAdviser from "@/components/common/contact-adviser.vue";
  import SearchMini from "@/components/search/search-mini.vue";
  import utils from "@/utils.js";
  import { useCustomFetch } from "@/composables/customFetch";

  // Lazy-load heavy below-the-fold components so they are code-split into
  // separate chunks and only downloaded/parsed after course data has loaded.
  const GradeDistribution = defineAsyncComponent(
    () => import("@/components/course/grade-distribution.vue"),
  );
  const OutcomeIndex = defineAsyncComponent(
    () => import("@/components/course/outcome-index.vue"),
  );
  const PrereqMap = defineAsyncComponent(
    () => import("@/components/course/prereq-map.vue"),
  );
  const ConcurrentCourses = defineAsyncComponent(
    () => import("@/components/course/concurrent-courses.vue"),
  );

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
      SearchMini,
    },
    data() {
      return {
        courseData: undefined,
        courseId: undefined,
        courseTitle: undefined,
        courseCampus: undefined,
        showError: false,
        loading: false,
      };
    },
    computed: {
      pageTitle() {
        if (this.courseTitle) return this.courseTitle;
        return this.showError ? "Error" : "Course";
      },
    },
    watch: {
      // Side effect kept out of computed — update document title when courseTitle changes
      courseTitle(val) {
        if (val) document.title = val + " - DawgPath";
      },
      courseId(newValue) {
        this.get_course_data(newValue);
      },
    },
    mounted() {
      this.courseId = this.$route.query.id;
      this.courseCampus = this.$route.query.campus;

      if (!this.courseId) {
        this.showError = true;
      }

      // Listen for course changes emitted by child components (e.g. prereq graph node clicks)
      this.emitter.on("update:selected", (selectedKey) => {
        this.courseId = selectedKey;
      });
    },
    beforeUnmount() {
      // Remove listener to prevent duplicate handlers if component remounts
      this.emitter.off("update:selected");
    },
    methods: {
      async get_course_data(course_id) {
        this.courseData = undefined;
        this.showError = false;
        this.loading = true;
        try {
          const data = await useCustomFetch(
            "/api/v1/courses/details/" + course_id,
          );
          this.courseData = data;
          this.courseCampus = data.course_campus;
          this.courseTitle = this.courseId + ": " + data.course_title;
          utils.recentViewManager(
            this.courseId,
            "course?id=" + this.courseId,
            this.courseCampus,
          );
        } catch {
          this.showError = true;
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>
