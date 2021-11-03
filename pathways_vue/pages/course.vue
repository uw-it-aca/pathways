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
          <search-course v-model:selected="courseId" />
        </div>
      </div>

      <div v-if="courseData">
        <div class="row">
          <div class="col-8"><course-details :course="courseData" /></div>
          <div class="col-4"><explore-course /></div>
        </div>
        <div class="row">
          <div class="col">
            <grade-distribution
            :course="courseData"/>
          </div>
          <div class="col">
            <outcome-index />
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
import SearchCourse from '../components/search/course.vue';
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
      courseData: {},
      courseId: undefined
    };
  },
  computed: {
  },
  mounted(){
    let course_id = this.$route.query.code;
    this.courseId = course_id;
    this.emitter.on("update:selected", selectedKey => {
      this.courseId = selectedKey;

    })
  },
  methods: {
    get_course_data(course_id){
      const vue = this;
      this.axios.get("/api/v1/courses/" + course_id).then((response) => {
        vue.courseData = response.data;
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
