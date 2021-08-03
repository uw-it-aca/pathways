// course.vue

<template>
  <div class="input-group">
    <input
      type="text"
      list="courses"
      v-model="course"
      class="form-control"
      aria-label=""
      placeholder="Enter a course code"
    />
    <button type="button" class="btn btn-purple" @click="searchCourse">Search</button>
  </div>
  <datalist id="courses">
    <option v-for="(course, i) in courses" :key="i">{{ course }}</option>
  </datalist>
</template>

<script>
import courseData from "./courses.json";

export default {
  name: 'SearchMajor',
  data() {
    return {
      course: '',
      courses: courseData
    };
  },
  methods: {
    searchCourse(event) {
      // TODO: wire up submit for course search
      alert('wire me up!');
    },
  },
};
</script>

<style lang="scss"></style>
