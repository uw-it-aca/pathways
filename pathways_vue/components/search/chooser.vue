// chooser.vue

<template>
  <div class="card bg-light">
    <div class="card-body">
      <h4 class="fw-bold mt-2">Search for a major or course</h4>

      <div class="my-3">
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault1"
          />
          <label class="form-check-label" for="flexRadioDefault1">Seattle Campus</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault2"
          />
          <label class="form-check-label" for="flexRadioDefault2">Tacoma Campus</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault3"
          />
          <label class="form-check-label" for="flexRadioDefault3">Bothell Campus</label>
        </div>
      </div>
      <div class="input-group my-3">
        <select class="form-select" id="inputGroupSelect01" disabled>
          <option selected>Select...</option>
          <option value="1">Major</option>
          <option value="2">Course</option>
        </select>
        <!-- TODO: change placeholder text based on user selection, disable search button until user selects major or course -->
        <!-- if none, placeholder blank
        if major selected: please enter amajor 
        if course selected: please enter a course-->
        <input type="text" class="form-control w-75" placeholder="Please enter a major" aria-label="Text input with dropdown button" />
        <button type="button" class="btn btn-purple" disabled @click="onSelected">Search</button>
      </div>
    </div>
  </div>
</template>
      <!--
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
      <search-major v-if="selectedRadio === 'major'" />
      <search-course :course-list="courseList" v-if="selectedRadio === 'course'" />
         -->

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

<style lang="scss">
</style>
