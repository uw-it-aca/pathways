// chooser.vue

<template>
  <div class="card bg-light mt-5">
    <div class="card-body">
      <h2 class="fw-bold mt-2 fs-5">Search for a major or course</h2>
      <form @submit.prevent="onSelected" role="search">
        <fieldset>
          <legend class="visually-hidden">Select a campus to search</legend>
          <div class="my-3">
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                name="flexRadioDefault"
                id="SeattleCampus"
                v-model="selectedCampus"
                value="seattle"
              />
              <label class="form-check-label" for="SeattleCampus"
                >Seattle</label
              >
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                name="flexRadioDefault"
                id="TacomaCampus"
                v-model="selectedCampus"
                value="tacoma"
              />
              <label class="form-check-label" for="TacomaCampus">Tacoma</label>
            </div>
            <div class="form-check form-check-inline">
              <input
                class="form-check-input"
                type="radio"
                name="flexRadioDefault"
                id="BothellCampus"
                v-model="selectedCampus"
                value="bothell"
              />
              <label class="form-check-label" for="BothellCampus"
                >Bothell</label
              >
            </div>
          </div>
        </fieldset>

        <div v-if="mq.smPlus" :class="selectedCampus ? 'enabled' : 'disabled'">
          <div class="input-group my-3">
            <select
              aria-label="Select major or course"
              class="form-select"
              id="inputGroupSelect01"
              v-model="searchType"
              style="max-width: 110px"
            >
              <option value="" selected disabled hidden>Select...</option>
              <option
                v-for="(option, index) in searchTypeOptions"
                v-bind:value="option.value"
                :key="index"
              >
                {{ option.text }}
              </option>
            </select>
            <!-- TODO: wire is-invalid class to datalist validation -->

            <input
              type="text"
              class="form-control rounded-end"
              :class="isValidInput || isValidInput == null ? '' : 'is-invalid'"
              :placeholder="searchPlaceholder"
              aria-autocomplete="list"
              autocomplete="off"
              aria-label="Start typing for major or course search options"
              v-model="selectedLabel"
              list="searchDataList"
              :disabled="searchType.length === 0"
              id="searchInput"
              @change="validateInput"
              @keypress="validateInput"
              @keydown="disableEnter($event)"
            />
            <div class="invalid-feedback text-end">
              Please clear and select from the dropdown options
            </div>
          </div>
          <div class="text-end mt-4">
            <button
              class="btn btn-outline-purple rounded-end me-2"
              :disabled="selectedLabel.length === 0"
              @click="clearInput"
            >
              Clear
            </button>
            <button
              type="button"
              class="btn btn-purple"
              :disabled="
                searchType.length === 0 ||
                loadingList ||
                !isValidInput ||
                !this.searchValue
              "
              @click="onSelected"
            >
              Search
            </button>
          </div>
        </div>

        <div
          v-else
          class="my-3"
          :class="selectedCampus ? 'enabled' : 'disabled'"
        >
          <select
            aria-label="Select major or course"
            class="form-select mb-2"
            id="inputGroupSelect01"
            v-model="searchType"
          >
            <option value="" selected disabled hidden>Select...</option>
            <option
              v-for="(option, index) in searchTypeOptions"
              v-bind:value="option.value"
              :key="index"
            >
              {{ option.text }}
            </option>
          </select>

          <input
            class="form-control mb-2"
            :class="isValidInput || isValidInput == null ? '' : 'is-invalid'"
            :placeholder="searchPlaceholder"
            aria-autocomplete="list"
            autocomplete="off"
            aria-label="Start typing for major or course search options"
            v-model="selectedLabel"
            list="searchDataList"
            :disabled="searchType.length === 0"
            id="searchInput"
            @change="validateInput"
            @keypress="validateInput"
            @keydown="disableEnter($event)"
          />

          <div class="invalid-feedback text-end">
            Please clear and select from the dropdown options
          </div>

          <div class="text-end mt-4">
            <button
              class="btn btn-outline-purple rounded-end me-2"
              :disabled="selectedLabel.length === 0"
              @click="clearInput"
            >
              Clear
            </button>
            <button
              type="button"
              class="btn btn-purple rounded-end"
              :disabled="
                searchType.length === 0 ||
                loadingList ||
                !isValidInput ||
                !this.searchValue
              "
              @click="onSelected"
            >
              Search
            </button>
          </div>
        </div>

        <datalist id="searchDataList">
          <option
            v-for="(option, i) in renderableOptions"
            :value="option"
            :key="i"
          >
            {{ option }}
          </option>
        </datalist>
      </form>
    </div>
  </div>

  <data-update />
</template>
<script>
import DataUpdate from "../common/data-update.vue";
export default {
  inject: ["mq"],
  name: "SearchChooser",
  components: {
    "data-update": DataUpdate,
  },
  props: {
    syncQueryParam: {
      default: null,
      type: String,
    },
    prefillId: {
      default: null,
      type: String,
    },
    prefillCampus: {
      default: null,
      type: String,
    },
    prefillType: {
      default: null,
      type: String,
    },
  },
  data() {
    return {
      selectedCampus: false,
      searchTypeOptions: [
        { text: "Major", value: "major" },
        { text: "Course", value: "course" },
      ],
      searchType: "",
      majorList: [],
      courseList: [],
      loadingList: false,
      selectedLabel: "",
      doPrefill: false,
      isValidInput: null,
    };
  },
  computed: {
    searchPlaceholder() {
      if (this.searchType === "major") {
        return "Start typing to select a major...";
      } else if (this.searchType === "course") {
        return "Start typing to select a course...";
      } else {
        return "Please select a campus...";
      }
    },
    renderableOptions() {
      let options = "";
      if (this.searchType === "major") {
        options = this.majorList.map((m) => m.value).sort();
      } else if (this.searchType === "course") {
        options = this.courseList.map((m) => m.value).sort();
      }
      return options;
    },
    selectedKey() {
      let searchList = {};
      if (this.searchType === "major") {
        searchList = this.majorList;
      } else if (this.searchType === "course") {
        searchList = this.courseList;
      }
      let selectedObj = searchList.find((o) => o.value === this.selectedLabel);
      if (selectedObj !== undefined) {
        return selectedObj.key;
      } else {
        return searchList;
      }
    },
    searchValue() {
      return this.selectedLabel;
    },
  },
  watch: {
    searchType(type) {
      this.selectedLabel = "";
      if (type === "major") {
        this.loadingList = true;
        this.fetch_major_data();
      } else if (type === "course") {
        this.loadingList = true;
        this.fetch_course_data();
      }
    },
    selectedCampus() {
      // reset selected type (don't reset on prefill initialization)
      if (!this.doPrefill) {
        this.searchType = "";
        this.selectedLabel = "";
      }
    },
    /*
    prefillCampus() {
      console.log("prefillCampus");
      this.selectedCampus = this.prefillCampus;
      if (this.prefillType === "major") {
        this.fetch_major_data();
      } else if (this.prefillType === "course") {
        this.fetch_course_data();
      }
      this.doPrefill = true;
    },
    */
    majorList() {
      if (this.doPrefill) {
        this.prefillForm();
      }
    },
    courseList() {
      if (this.doPrefill) {
        this.prefillForm();
      }
    },
    prefillCampus() {
      // console.log("prefillCampus");
      this.startPrefill();
    },
  },
  methods: {
    startPrefill() {
      console.log("startPrefill");
      if (
        this.prefillCampus !== null &&
        this.prefillType !== null &&
        this.prefillId !== null
      ) {
        this.doPrefill = true;
        this.selectedCampus = this.prefillCampus;
        this.searchType = this.prefillType;
      }
    },
    prefillForm() {
      let prefillLabel = undefined;
      let searchList = {};
      if (this.searchType === "major") {
        searchList = this.majorList;
      } else if (this.searchType === "course") {
        searchList = this.courseList;
      }
      let selectedObj = searchList.find((o) => o.key === this.prefillId);
      if (selectedObj !== undefined) {
        prefillLabel = selectedObj.value;
      }
      this.selectedLabel = prefillLabel;
      this.doPrefill = false;
    },
    onSelected() {
      let url = "/" + this.searchType;
      this.$router.push({
        path: url,
        query: { ["id"]: this.selectedKey, ["campus"]: this.selectedCampus },
      });

      this.$emit("update:selected", {
        id: this.selectedKey,
        campus: this.selectedCampus,
      });
    },

    fetch_course_data() {
      const vue = this;
      this.axios
        .get("/api/v1/courses/" + this.selectedCampus)
        .then((response) => {
          vue.courseList = response.data;
          this.loadingList = false;
        });
    },
    fetch_major_data() {
      const vue = this;
      this.axios
        .get("/api/v1/majors/" + this.selectedCampus)
        .then((response) => {
          vue.majorList = response.data;
          this.loadingList = false;
        });
    },
    validateInput() {
      let found;

      // clear validation for empty inputs
      if (this.searchValue == "") {
        this.isValidInput = true;
        return;
      }

      // search for the searchValue based on search type
      if (this.searchType == "major") {
        found = Array.from(this.majorList).find(
          (element) => element.value == this.searchValue
        );
      } else {
        found = Array.from(this.courseList).find(
          (element) => element.value == this.searchValue
        );
      }

      // set validation based on the found value
      if (found != undefined && found.value) {
        this.isValidInput = true;
      } else {
        this.isValidInput = false;
      }
    },
    disableEnter(e) {
      if (e.keyCode == 13) {
        // this.validateInput();
        e.preventDefault();
        return false;
      }
    },
    clearInput() {
      //this.searchType = "";
      this.selectedLabel = "";
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
  appearance: none;
  text-indent: 1px;
}
</style>
