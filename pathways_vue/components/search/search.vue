// course.vue

<template>
  <div class="card bg-light mt-5">
    <!--  Search Bar  -->
    <div class="card-body" @click="openSearch">
      <form @submit.prevent="onSelected" role="search">
        <i class="bi bi-search" @click="runSearch"></i>
        <div class="form-group">
          <input
            type="text"
            v-model="form_data.search_string"
            class="form-control"
            id="search-string"
            placeholder="Start typing to search for courses, majors, or subjects"
          >
          <a href="#" @click.prevent="clearSearch">Clear</a>
        </div>
        <template v-if="show_filters">
          <div class="btn-group-toggle" data-toggle="buttons">
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
          <div class="btn-group-toggle" data-toggle="buttons">
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
        </template>
        <button type="submit" @click="runSearch">Search</button>
      </form>
      <p v-if="search_error">Error running search</p>
    </div>
    <i @click="closeSearch" class="bi bi-x-circle-fill"></i>
    <template v-if="show_search">
      <results v-if="show_results" :search_results="search_results"/>
      <template v-else>
        <recent-views/>
        <recent-searches @set-search="setSearch"/>
      </template>
    </template>
    <div>
    </div>
  </div>
</template>
<script>
import RecentSearches from "./recent_searches.vue";
import RecentViews from "./recent_views.vue";
import Results from "./results.vue";

export default {
  name: 'Search',
  components: {
    RecentSearches,
    RecentViews,
    Results,
  },
  props: {
  },
  data() {
    return {
      form_data: {
        search_string: "",
        campus: [],
        type: [],
      },
      major_matches: [],
      course_matches: [],
      text_matches: [],
      show_search: false,
      search_error: false
    };
  },
  computed: {
    search_results(){
      return this.major_matches.concat(this.course_matches).concat(this.text_matches);
    },
    show_filters() {
      return this.form_data.search_string.length > 0 && this.show_search;
    },
    show_results() {
      return this.search_results.length > 0;
    }
  },
  watch: {
  },
  methods: {
    openSearch(){
      this.show_search = true;
    },
    closeSearch(){
      this.show_search = false;
    },
    clearSearch(){
      this.form_data.search_string = "";
      this.major_matches = [];
      this.course_matches = [];
      this.text_matches = [];
    },
    updateValues(e) {
      this.form_data.min_coi_score = e.minValue;
      this.form_data.max_coi_score = e.maxValue;
    },
    runSearch(){
      const vue = this;
      this.addToRecent(this.form_data.search_string);
      this.axios.get("api/v1/search/", {
        params: vue.form_data,
      }).then((response) => {
        this.course_matches = response.data.course_matches;
        this.major_matches = response.data.major_matches;
        this.text_matches = response.data.text_matches;
        this.search_error = false;
      }).catch((error) => {
        this.search_error = true;
      });
    },
    addToRecent(searchString){
      let currentRecentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];
      // add the new view to the front of the array
      if (!currentRecentSearches.includes(searchString)){
        currentRecentSearches.unshift(searchString)
      }
      // keep the array to 5 items
      if (currentRecentSearches.length > 5){
        currentRecentSearches = currentRecentSearches.slice(0, 5)
      }
      localStorage.setItem('recentSearches', JSON.stringify(currentRecentSearches));
    },
    setSearch(search_string){
      this.form_data.search_string = search_string;
      this.runSearch();
    },

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
</style>
