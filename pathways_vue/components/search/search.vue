// course.vue

<template>
  <button
    type="button"
    class="btn btn-primary"
    data-bs-toggle="modal"
    data-bs-target="#searchModal"
    @click="openSearch"
  >
    <i class="bi bi-search"></i>
    <span>style faux search bar (button)</span>
  </button>

  <!-- Modal -->
  <div
    class="modal fade"
    id="searchModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div
      class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable"
    >
      <div class="modal-content">
        <div class="modal-header">
          <!-- search bar -->
          <form @submit.prevent="onSelected" role="search" class="w-100">
            <div class="d-flex flex-fill">
              <div class="w-100">
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-search"></i
                  ></span>
                  <input
                    type="text"
                    role="search"
                    class="form-control focus-ring"
                    id="search-string"
                    autocomplete="off"
                    autocorrect="off"
                    autocapitalize="off"
                    enterkeyhint="go"
                    spellcheck="false"
                    placeholder="Search here"
                    v-model="form_data.search_string"
                    aria-label="Recipient's username"
                    aria-describedby="button-addon2"
                  />
                  <button
                    class="btn btn-primary"
                    id="button-addon2"
                    type="submit"
                    @click="runSearch"
                  >
                    Search
                  </button>
                </div>
              </div>
            </div>

            <template v-if="show_filters">
              <div class="border border-danger d-flex mt-3">
                <div class="btn-group-toggle" data-toggle="buttons">
                  <h4>Type</h4>
                  <label class="btn btn-secondary active">
                    <input
                      id="course"
                      value="course"
                      v-model="form_data.type"
                      type="checkbox"
                      autocomplete="off"
                    />
                    Course
                  </label>
                  <label class="btn btn-secondary active">
                    <input
                      id="major"
                      value="major"
                      v-model="form_data.type"
                      type="checkbox"
                      autocomplete="off"
                    />
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
                      autocomplete="off"
                    />
                    Seattle
                  </label>
                  <label class="btn btn-secondary active">
                    <input
                      id="tacoma"
                      value="tacoma"
                      v-model="form_data.campus"
                      type="checkbox"
                      autocomplete="off"
                    />
                    Tacoma
                  </label>
                  <label class="btn btn-secondary active">
                    <input
                      id="bothell"
                      value="bothell"
                      v-model="form_data.campus"
                      type="checkbox"
                      autocomplete="off"
                    />
                    Bothell
                  </label>
                </div>
                <div class="ms-auto">
                  <a href="#" @click.prevent="clearSearch">Clear results</a>
                </div>
              </div>
            </template>
          </form>
        </div>
        <div class="modal-body" style="max-height: 500px">
          <template v-if="show_search">
            <results v-if="show_results" :search_results="search_results" />
            <template v-else>
              <recent-views />
              <recent-searches @set-search="setSearch" />
            </template>
          </template>
        </div>
        <div class="modal-footer">footer optional?</div>
      </div>
    </div>
  </div>
  <!-- end Modal -->

  <!-- MAR: not needed at the moment -->
  <i @click="closeSearch" class="d-none bi bi-x-circle-fill">close results</i>
</template>
<script>
import RecentSearches from "./recent_searches.vue";
import RecentViews from "./recent_views.vue";
import Results from "./results.vue";

export default {
  name: "SearchComponent",
  components: {
    RecentSearches,
    RecentViews,
    Results,
  },
  props: {},
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
      search_error: false,
      has_searched: false,
    };
  },
  computed: {
    search_results() {
      return this.major_matches
        .concat(this.course_matches)
        .concat(this.text_matches);
    },
    show_filters() {
      return this.form_data.search_string.length > 0 && this.show_search;
    },
    show_results() {
      return this.search_results.length > 0 || this.has_searched;
    },
    search_string() {
      return this.form_data.search_string.trim();
    },
  },
  watch: {},
  methods: {
    openSearch() {
      this.show_search = true;
    },
    closeSearch() {
      this.show_search = false;
    },
    clearSearch() {
      this.form_data.search_string = "";
      this.clearResults();
      this.has_searched = false;
    },
    clearResults() {
      this.major_matches = [];
      this.course_matches = [];
      this.text_matches = [];
    },
    updateValues(e) {
      this.form_data.min_coi_score = e.minValue;
      this.form_data.max_coi_score = e.maxValue;
    },
    runSearch() {
      const vue = this;
      this.clearResults();
      this.addToRecent(this.search_string);
      this.axios
        .get("api/v1/search/", {
          params: vue.form_data,
        })
        .then((response) => {
          this.course_matches = response.data.course_matches;
          this.major_matches = response.data.major_matches;
          this.text_matches = response.data.text_matches;
          this.search_error = false;
          this.has_searched = true;
        })
        .catch((error) => {
          this.search_error = true;
        });
    },
    addToRecent(searchString) {
      if (searchString.length === 0) {
        return;
      }
      let currentRecentSearches =
        JSON.parse(localStorage.getItem("recentSearches")) || [];
      // add the new view to the front of the array
      if (!currentRecentSearches.includes(searchString)) {
        currentRecentSearches.unshift(searchString);
      }
      // keep the array to 5 items
      if (currentRecentSearches.length > 5) {
        currentRecentSearches = currentRecentSearches.slice(0, 5);
      }
      localStorage.setItem(
        "recentSearches",
        JSON.stringify(currentRecentSearches)
      );
    },
    setSearch(search_string) {
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
