// chooser.vue

<template>
  <div class="card bg-light mb-5">
    <div class="card-body">
      <p>Search for a...</p>

      <div class="form-check form-check-inline">
        <input
          class="form-check-input"
          type="radio"
          name="flexRadioDefault"
          id="flexRadioDefault1"
        />
        <label class="form-check-label" for="flexRadioDefault1">
          Major
        </label>
      </div>
      <div class="form-check form-check-inline">
        <input
          class="form-check-input"
          type="radio"
          name="flexRadioDefault"
          id="flexRadioDefault2"
          checked
        />
        <label class="form-check-label" for="flexRadioDefault2">
          Course
        </label>
      </div>

      <search-major />
      <search-course />
    </div>
  </div>
</template>

<script>
import SearchMajor from './major.vue';
import SearchCourse from './course.vue';

export default {
  name: "SearchChooser",
  components: {
    'search-major': SearchMajor,
    'search-course': SearchCourse
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style lang="scss"></style>
