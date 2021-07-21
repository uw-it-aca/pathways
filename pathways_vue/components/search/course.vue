// course.vue

<template>
  <div class="input-group">
    <input type="text" class="form-control" aria-label="" placeholder="Enter a course code" />
    <button type="button" class="btn btn-purple" @click="searchCourse">Search</button>
  </div>
</template>

<script>

export default {
  name: "SearchMajor",
  data() {
    return {};
  },
  methods: {
    searchCourse(event) {
      // TODO: wire up submit for course search
      alert('wire me up!')
    }
  }
};
</script>

<style lang="scss"></style>
