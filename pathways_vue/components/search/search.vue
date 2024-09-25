// course.vue

<template>
  <div class="my-5 row justify-content-center">
    <button
      type="button"
      class="btn btn-lg btn-link border-purple border-2 text-start w-75 bg-transparent-hover text-decoration-none mx-auto"
      @keydown.tab.exact="false"
      @keydown.exact="handleKeyboard"
      @click="openSearch"
    >
      <i class="bi bi-search me-3 text-secondary"></i>
      <span class="text-secondary"
        >Start typing to search for courses, majors, or subjects</span
      >
    </button>
  </div>
  <!-- Modal -->
  <div
    class="modal"
    id="searchModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <!-- custom search bar -->
          <form @submit.prevent="onSelected" role="search" class="w-100">
            <div class="d-flex flex-fill">
              <div class="w-100">
                <div class="position-relative">
                  <i
                    class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-secondary"
                  ></i>
                  <input
                    type="text"
                    role="search"
                    class="form-control form-control-lg px-5 mb-2 border-purple border-2"
                    id="search-string"
                    autocomplete="off"
                    autocorrect="off"
                    autocapitalize="off"
                    enterkeyhint="go"
                    spellcheck="false"
                    placeholder="Start typing to search for courses, majors, or subjects"
                    v-model="form_data.search_string"
                    aria-label="Recipient's username"
                    aria-describedby="button-addon2"
                    @input="debouncedSearch"
                  />
                  <button
                    v-if="show_results"
                    type="button"
                    @click="clearSearch"
                    class="btn btn-link text-secondary text-purple-hover position-absolute top-50 end-0 translate-middle-y p-1 me-2"
                  >
                    clear
                  </button>
                </div>
                <!-- MARK: remove search button -->
                <button
                  class="btn btn-primary visually-hidden"
                  id="button-addon2"
                  type="submit"
                  @click="runSearch"
                >
                  Search
                </button>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-body" style="max-height: 600px">
          <template v-if="show_recent">
            <template v-if="show_results">
              <div class="d-flex">
                <div class="me-3">
                  <div>
                    <label class="form-label small fw-bold me-2">Type</label>
                  </div>
                  <ul class="list-inline">
                    <li class="list-inline-item mb-1 me-1">
                      <input
                        id="course"
                        value="course"
                        v-model="form_data.type"
                        type="checkbox"
                        autocomplete="off"
                        class="btn-check"
                        @change="runSearch"
                      />
                      <label
                        class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                        for="course"
                        >Course</label
                      >
                    </li>
                    <li class="list-inline-item mb-1 me-1">
                      <input
                        id="major"
                        value="major"
                        v-model="form_data.type"
                        type="checkbox"
                        autocomplete="off"
                        class="btn-check"
                        @change="runSearch"
                      />
                      <label
                        class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                        for="major"
                        >Major</label
                      >
                    </li>
                  </ul>
                </div>
                <div class="btn-group-toggle" data-toggle="buttons">
                  <div>
                    <label class="form-label small fw-bold me-2">Campus</label>
                  </div>
                  <ul class="list-inline">
                    <li class="list-inline-item mb-1 me-1">
                      <input
                        id="seattle"
                        value="seattle"
                        v-model="form_data.campus"
                        type="checkbox"
                        autocomplete="off"
                        class="btn-check"
                        @change="runSearch"
                      />
                      <label
                        class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                        for="seattle"
                        >Seattle</label
                      >
                    </li>
                    <li class="list-inline-item mb-1 me-1">
                      <input
                        id="tacoma"
                        value="tacoma"
                        v-model="form_data.campus"
                        type="checkbox"
                        autocomplete="off"
                        class="btn-check"
                        @change="runSearch"
                      />
                      <label
                        class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                        for="tacoma"
                        >Tacoma</label
                      >
                    </li>
                    <li class="list-inline-item mb-1 me-1">
                      <input
                        id="bothell"
                        value="bothell"
                        v-model="form_data.campus"
                        type="checkbox"
                        autocomplete="off"
                        class="btn-check"
                        @change="runSearch"
                      />
                      <label
                        class="btn btn-sm btn-outline-dark-beige fs-9 rounded-pill"
                        for="bothell"
                        >Bothell</label
                      >
                    </li>
                  </ul>
                </div>
              </div>
            </template>
            <results v-if="show_results" :search_results="search_results" />
            <template v-else>
              <div class="container-md">
                <div class="row">
                  <div class="col">
                    <recent-searches @set-search="setSearch" />
                  </div>
                  <div class="col">
                    <recent-views />
                  </div>
                </div>
              </div>
            </template>
          </template>
        </div>
        <!-- <div class="modal-footer">footer optional?</div> -->
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
import debounce from "debounce";
import { Modal } from "bootstrap";

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
      show_recent: false,
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
    /*show_filters() {
      return this.form_data.search_string.length > 0 && this.show_recent;
    },*/
    show_results() {
      return this.search_results.length > 0 || this.has_searched;
    },
    search_string() {
      return this.form_data.search_string.trim();
    },
  },
  watch: {},
  methods: {
    handleKeyboard(e) {
      // guard against tab presses when focused
      if (e.key !== "Tab") {
        // open the search modal
        this.openSearch();
        return;
      }
    },
    openSearch() {
      // initialize modal
      this.searchModal = new Modal(document.getElementById("searchModal"), {});
      this.searchModal.show();

      // clear original search results
      this.clearSearch();

      // show recent search panel
      this.show_recent = true;
    },
    closeSearch() {
      this.show_recent = false;
    },
    clearSearch() {
      this.form_data.search_string = "";
      this.clearResults();
      this.has_searched = false;

      // set focus back on search input when clearing
      document.getElementById("search-string").focus();
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
    debouncedSearch: debounce(function () {
      this.runSearch();
    }, 500),
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
          console.log(error);
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
  mounted() {
    const searchModal = document.getElementById("searchModal");
    const searchInput = document.getElementById("search-string");

    searchModal.addEventListener("shown.bs.modal", () => {
      searchInput.focus();
    });
  },
};
</script>

<style lang="scss">
.disabled {
  pointer-events: none;
  opacity: 0.4;
}

.form-select {
  text-indent: 1px;
  appearance: none;
}

.blah:focus {
  outline: none !important;
  box-shadow: none !important;
  border-color: gray !important;
}
</style>
