// course.vue

<template>
  <div class="card bg-light mt-5">
    <!--  Search Bar  -->
    <div class="card-body">
      <form @submit.prevent="onSelected" role="search">
        <div class="form-group">
          <input
            type="text"
            v-model="form_data.search_string"
            class="form-control"
            id="search-string"
            placeholder="Start typing to search for courses, majors, or subjects"
            @focus="input_active = true"
            @blur="input_active = false"
          >
        </div>
        <div v-if="show_filters" class="btn-group-toggle" data-toggle="buttons">
          <h4>Type</h4>
          <label class="btn btn-secondary active">
            <input
              id="course"
              value="course"
              v-model="form_data.type"
              type="checkbox"
              autocomplete="off">
            Course
          </label>
          <label class="btn btn-secondary active">
            <input
              id="major"
              value="major"
              v-model="form_data.type"
              type="checkbox"
              autocomplete="off">
            Major
          </label>
        </div>
        <div v-if="show_filters" class="btn-group-toggle" data-toggle="buttons">
          <h4>Campus</h4>
          <label class="btn btn-secondary active">
            <input
              id="seattle"
              value="seattle"
              v-model="form_data.campus"
              type="checkbox"
              autocomplete="off">
            Seattle
          </label>
          <label class="btn btn-secondary active">
            <input
              id="tacoma"
              value="tacoma"
              v-model="form_data.campus"
              type="checkbox"
              autocomplete="off">
            Tacoma
          </label>
          <label class="btn btn-secondary active">
            <input
              id="bothell"
              value="bothell"
              v-model="form_data.campus"
              type="checkbox"
              autocomplete="off">
            Bothell
          </label>
        </div>
        <button type="submit" @click="runSearch">Search</button>
      </form>
    </div>
    <!--  Results  -->
    <div>
      <h2>Results - {{ result_count }}</h2>
      <ul>
        <li v-for="result in search_results" :key="result.id">
          {{ result.score }} - {{ result.contents }}
        </li>
      </ul>
    </div>
    <recent-views/>
    <div>

    </div>
    <recent-searches/>
    <div>

    </div>
  </div>
</template>
<script>
import qs from "qs";
import RecentSearches from "./recent_searches.vue";
import RecentViews from "./recent_views.vue";

export default {
  name: 'Search',
  components: {
    RecentSearches,
    RecentViews
  },
  props: {
  },
  data() {
    return {
      form_data: {
        search_string: "",
        campus: [],
        type: [],
        is_gateway: null,
        is_bottleneck: null,
        min_coi_score: 0,
        max_coi_score: 5,
      },
      input_active: false,
      major_matches: [],
      course_matches: [],
      text_matches: [],
    };
  },
  computed: {
    result_count() {
      if (this.search_results === null) {
        return 0;
      } else {
        return this.search_results.length;
      }
    },
    search_results(){
      return this.major_matches.concat(this.course_matches).concat(this.text_matches);
    },
    show_filters() {
      return this.form_data.search_string.length > 0 || this.input_active
    }
  },
  watch: {
  },
  methods: {
    updateValues(e) {
      this.form_data.min_coi_score = e.minValue;
      this.form_data.max_coi_score = e.maxValue;
    },
    runSearch(){
      const vue = this;
      this.axios.get("api/v1/search/", {
        params: vue.form_data,
        paramsSerializer: params => {
          return qs.stringify(params, {skipNulls: true})
        }
      }).then((response) => {
        this.course_matches = response.data.course_matches;
        this.major_matches = response.data.major_matches;
        this.text_matches = response.data.text_matches;
      });
    }
  },
};
</script>

<style lang="scss">

.disabled {
    pointer-events: none;
    opacity: 0.4;
}

.form-select {
  -webkit-appearance: none;
  -moz-appearance: none;
  text-indent: 1px;
}

.coi-slider-container {
  max-width: 300px;
  margin-top: 50px;
  margin-bottom: 20px;
}


.coi-range-slider {
  display: flex;
	position: relative;
	border: none;
	border-radius: 0px;
	padding: 10px;
	box-shadow: none;
	flex-direction: column;
	-webkit-touch-callout: none; /* iOS Safari */
	-webkit-user-select: none; /* Safari */
	-khtml-user-select: none; /* Konqueror HTML */
	-moz-user-select: none; /* Old versions of Firefox */
	-ms-user-select: none; /* Internet Explorer/Edge */
	user-select: none; /* Non-prefixed version, currently supported by Chrome, Edge,*/
}

.coi-range-slider .caption {
	position: absolute;
	bottom: 45px;
	width: 2px;
	height: 2px;
	left: 1px;
	display: flex;
	justify-content: center;
	align-items: center;
	overflow: visible;
	/* display: none; */
}
.coi-range-slider .thumb .caption * {
	position: absolute;
	min-width: 30px;
	height: 30px;
	font-size: 75%;
	text-align: center;
	line-height: 30px;
	background-color: blue;
	border-radius: 5px;
	color: white;
	box-shadow: 0px 0px 5px black;
	padding: 0px 5px;
	white-space: nowrap;
}


</style>
