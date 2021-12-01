// course.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title
      ><h1 class="visually-hidden">{{ pageTitle }}</h1></template
    >
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
        <div class="row">
          <div class="col-sm-8"><course-details :course="courseData" /></div>
          <div class="col-sm-4"><explore-course :course="courseData"/></div>
        </div>
        <div class="row">
          <div class="col-sm-6">
            <grade-distribution
            :course="courseData"/>
          </div>
          <div class="col-sm-6">
            <outcome-index
            :course="courseData"/>
          </div>
        </div>

        <prereq-map
        :graph_data="courseData.prereq_graph"
        :active_course="courseId"
        />
        <concurrent-courses :courseData="courseData"/>
        <contact-adviser-course />
      </div>
      <div v-else>PLACEHOLDER: select something</div>
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
import ContactAdviserCourse from '../components/course/contact-adviser-course.vue';

export default {
  components: {
    layout: Layout,
    'search-chooser': SearchChooser,
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
      courseData: {},
      courseId: undefined,
      courseCampus: undefined
    };
  },
  computed: {
  },
  mounted(){
    let course_id = this.$route.query.id;
    this.courseId = course_id;
    this.emitter.on("update:selected", selectedKey => {
      this.courseId = selectedKey;

    })
  },
  methods: {
    switch_course(data){
      this.courseId = data.id;
      this.courseCampus = data.campus
    },
    get_course_data(course_id){
      const vue = this;
      this.axios.get("/api/v1/courses/details/" + course_id).then((response) => {
        vue.courseData = response.data;
        vue.courseCampus = response.data.course_campus;
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
