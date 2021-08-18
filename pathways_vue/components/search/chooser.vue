// chooser.vue

<template>
  <div class="card bg-light">
    <div class="card-body">
      <p>Search for a...</p>

      <div class="mb-2">
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault1"
            v-model="selectedRadio"
            value="major"
            selected
          />
          <label class="form-check-label" for="flexRadioDefault1"> Major </label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault2"
            v-model="selectedRadio"
            value="course"
          />
          <label class="form-check-label" for="flexRadioDefault2"> Course </label>
        </div>
      </div>
      <search-major :major-list="majorList" v-if="selectedRadio === 'major'" />
      <search-course :course-list="courseList" v-if="selectedRadio === 'course'" />
    </div>
  </div>
</template>

<script>
import SearchMajor from './major.vue';
import SearchCourse from './course.vue';

export default {
  name: 'SearchChooser',
  components: {
    'search-major': SearchMajor,
    'search-course': SearchCourse,
  },
  props: {
    courseList: {
      type: Array,
      required: true,
    },
    majorList: {
      type: Array,
      required: true,
    }
  },
  data() {
    return {
      selectedRadio: 'major',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
