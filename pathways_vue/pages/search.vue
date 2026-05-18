<template>
  <DefaultLayout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <h1>Search</h1>
      <form @submit.prevent="runSearch" role="search" class="w-100">
        <div class="d-flex flex-fill">
          <div class="w-100">
            <div class="position-relative">
              <i
                class="bi bi-search position-absolute translate-middle-y start-0 top-50 ms-3"
              ></i>
              <input
                type="text"
                role="search"
                class="form-control form-control-lg mb-2 border-2 px-5"
                id="search-string"
                autocomplete="off"
                autocorrect="off"
                autocapitalize="off"
                enterkeyhint="go"
                spellcheck="false"
                v-model="form_data.search_string"
                aria-label="Recipient's username"
                aria-describedby="button-addon2"
              />
              <button
                v-if="show_results"
                type="button"
                @click="clearSearch"
                class="btn btn-link position-absolute translate-middle-y end-0 top-50 me-2 p-1"
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
            <div class="text-secondary">
              Press Enter to search for courses, majors, or subjects
            </div>
          </div>
        </div>
      </form>

      <template v-if="show_results">
        <div class="d-flex">
          <div class="me-3">
            <div>
              <label class="form-label small fw-bold me-2">Type</label>
            </div>
            <ul class="list-inline">
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="allType"
                  v-model="form_data.type"
                  name="type-radios"
                  value="all"
                  @change="runSearch"
                  >All
                </BFormRadio>
              </li>
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="courseType"
                  v-model="form_data.type"
                  name="type-radios"
                  value="course"
                  @change="runSearch"
                  >Course
                </BFormRadio>
              </li>
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="majorType"
                  v-model="form_data.type"
                  name="type-radios"
                  value="major"
                  @change="runSearch"
                  >Major
                </BFormRadio>
              </li>
            </ul>
          </div>
          <div class="btn-group-toggle" data-toggle="buttons">
            <div>
              <label class="form-label small fw-bold me-2">Campus</label>
            </div>
            <ul class="list-inline">
              <li class="list-inline-item me-1 mb-1">

                <BFormRadio
                  id="allCampus"
                  v-model="form_data.campus"
                  name="campus-radios"
                  value="all"
                  @change="runSearch"
                  >All
                </BFormRadio>
              </li>
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="seattleCampus"
                  v-model="form_data.campus"
                  name="campus-radios"
                  value="seattle"
                  @change="runSearch"
                  >Seattle
                </BFormRadio>

              </li>
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="tacomaCampus"
                  v-model="form_data.campus"
                  name="campus-radios"
                  value="tacoma"
                  @change="runSearch"
                  >Tacoma
                </BFormRadio>
              </li>
              <li class="list-inline-item me-1 mb-1">
                <BFormRadio
                  id="bothellCampus"
                  v-model="form_data.campus"
                  name="campus-radios"
                  value="bothell"
                  @change="runSearch"
                  >Bothell
                </BFormRadio>
              </li>
            </ul>
          </div>
        </div>

        <h2>Results</h2>
        <SearchResults v-if="show_results" :search_results="search_results" />
      </template>

      <template v-else>
        <div class="d-flex">
          <div class="w-50">
            <RecentSearches @set-search="setSearch" />
          </div>
          <div class="w-50"><RecentViews /></div>
        </div>
      </template>
    </template>
  </DefaultLayout>
</template>

<script>
  import DefaultLayout from "@/layouts/default.vue";
  import RecentSearches from "@/components/search/recent_searches.vue";
  import RecentViews from "@/components/search/recent_views.vue";
  import SearchResults from "@/components/search/results.vue";
  import { useCustomFetch } from "@/composables/customFetch";
  import { BFormRadio } from "bootstrap-vue-next";

  export default {
    components: {
      DefaultLayout,
      RecentSearches,
      RecentViews,
      SearchResults,
      BFormRadio,
    },
    props: {},
    data() {
      return {
        pageTitle: "Search",
        form_data: {
          search_string: "",
          campus: "all",
          type: "all",
        },
        major_matches: [],
        course_matches: [],
        text_matches: [],
        search_error: false,
        has_searched: false,
      };
    },
    computed: {
      search_results() {
        let results = this.major_matches
          .concat(this.course_matches)
          .concat(this.text_matches);

        if (this.form_data.type === "course") {
          results = results.filter((r) => r.is_course);
        } else if (this.form_data.type === "major") {
          results = results.filter((r) => r.is_major);
        }

        if (this.form_data.campus !== "all") {
          results = results.filter(
            (r) =>
              (r.campus || "").toLowerCase() === this.form_data.campus,
          );
        }

        return results;
      },
      show_results() {
        return this.search_results.length > 0 || this.has_searched;
      },
      search_string() {
        return this.form_data.search_string.trim();
      },
    },
    watch: {
      search_string(val) {
        this.$router.replace({ query: { ...this.$route.query, q: val || undefined } });
      },
    },
    methods: {
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
      async runSearch() {
        this.clearResults();
        this.addToRecent(this.search_string);

        const params = new URLSearchParams();
        params.set("search_string", this.form_data.search_string);
        if (this.form_data.type !== "all") {
          params.append("type[]", this.form_data.type);
        }
        if (this.form_data.campus !== "all") {
          params.append("campus[]", this.form_data.campus);
        }
        const url = "api/v1/search/?" + params.toString();

        try {
          const data = await useCustomFetch(url);
          this.course_matches = data.course_matches;
          this.major_matches = data.major_matches;
          this.text_matches = data.text_matches;
          this.search_error = false;
          this.has_searched = true;
        } catch (error) {
          this.search_error = true;
        }
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
          JSON.stringify(currentRecentSearches),
        );
      },
      setSearch(search_string) {
        this.form_data.search_string = search_string;
        this.runSearch();
      },
    },
    mounted() {
      const q = this.$route.query.q;
      if (q) {
        this.form_data.search_string = q;
        this.runSearch();
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
    text-indent: 1px;
  }

  .blah:focus {
    outline: none !important;
    box-shadow: none !important;
    border-color: gray !important;
  }
</style>
