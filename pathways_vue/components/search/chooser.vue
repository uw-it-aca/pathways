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
          <label class="form-check-label" for="SeattleCampus">Seattle Campus</label>
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
          <label class="form-check-label" for="TacomaCampus">Tacoma Campus</label>
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
          <label class="form-check-label" for="BothellCampus">Bothell Campus</label>
        </div>
      </div>
      </fieldset>
      <div class="input-group my-3" :class="selectedCampus ? 'enabled' : 'disabled'">
        <select aria-label="Select major or course" class="form-select" id="inputGroupSelect01" v-model="searchType" style="max-width: 110px;">
          <option value="" selected disabled hidden>Select...</option>
          <option v-for="option in searchTypeOptions" v-bind:value="option.value">
            {{option.text}}
          </option>
        </select>
        <!-- TODO: wire is-invalid class to datalist validation -->
        <input
          type="text"
          class="form-control"
          :class="isValidInput == null ? '' : 'is-invalid'"
          :placeholder="searchPlaceholder"
          aria-autocomplete="both"
          aria-label="Start typing for major or course search options"
          v-model="selectedLabel"
          list="searchDataList"
          :disabled="searchType.length === 0"
          required
          id="searchInput"
          @change="validateInput"
        />
        <button type="button"
                class="btn btn-purple"
                :disabled="searchType.length === 0 || loadingList || selectedLabel.length === 0"
                @click="onSelected">
          Go
        </button>
        <!-- TODO: update this message -->
        <div class="invalid-feedback">You must select a major/course from the list</div>
      </div>
      <datalist id="searchDataList">
        <option v-for="(option, i) in renderableOptions" :value="option" :key="i">{{ option }}</option>
      </datalist>
      </form>
    </div>
  </div>
</template>
<script>

export default {
  name: 'SearchChooser',
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
    }
  },
  data() {
    return {
      selectedCampus: false,
      searchTypeOptions: [
        {text: "Major", value:"major"},
        {text: "Course", value:"course"},
      ],
      searchType: "",
      majorList:[],
      courseList:[],
      loadingList: false,
      selectedLabel: "",
      doPrefill: false,
      isValidInput: null,
    };
  },
  computed: {
    searchPlaceholder() {
      if(this.searchType === "major"){
        return "Start typing to select a major (e.g. Math, Environmental Studies, design)"
      } else if(this.searchType === "course"){
        return "Start typing to select a course (e.g. CSE 142, Calculus, climate change)"
      } else {
        return "Please select a campus and a major or course"
      }
    },
    renderableOptions() {
      if(this.searchType==="major"){
        return this.majorList.map(m => m.value).sort();
      }else if(this.searchType==="course"){
        return this.courseList.map(m => m.value).sort();
      }
    },
    selectedKey() {
      let searchList = {};
      if(this.searchType==="major"){
        searchList = this.majorList;
      }else if(this.searchType==="course"){
        searchList = this.courseList;
      }
      let selectedObj = searchList.find(o => o.value === this.selectedLabel);
      if (selectedObj !== undefined){
        return selectedObj.key;
      }
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
    selectedCampus(){
      // reset selected type (don't reset on prefill initialization)
      if(!this.doPrefill){
        this.searchType = "";
        this.selectedLabel = "";
      }

    },
    prefillCampus(){
      this.selectedCampus = this.prefillCampus;
      if(this.prefillType==="major"){
        this.fetch_major_data()
      }else if(this.prefillType==="course"){
        this.fetch_course_data()
      }
      this.doPrefill = true;
    },
    majorList(){
      if(this.doPrefill){
        this.prefillForm();
      }
    },
    courseList(){
      if(this.doPrefill){
        this.prefillForm();
      }
    },
    prefillCampus(pc){
      this.startPrefill();
    }
  },
  methods: {
    startPrefill(){
      if(this.prefillCampus !== null
        && this.prefillType !== null
        && this.prefillId !== null) {
        this.doPrefill = true;
        this.selectedCampus = this.prefillCampus;
        this.searchType = this.prefillType;
      }
    },
    prefillForm() {
      let prefillLabel = undefined;
      let searchList = {};
      if(this.searchType==="major"){
        searchList = this.majorList;
      }else if(this.searchType==="course"){
        searchList = this.courseList;
      }
      let selectedObj = searchList.find(o => o.key === this.prefillId);
      if (selectedObj !== undefined){
        prefillLabel = selectedObj.value;
      }
      this.selectedLabel = prefillLabel;
      this.doPrefill = false;
    },
    onSelected() {
      let url = "/" + this.searchType;
      this.$router.push({
        path: url,
        query: { ['id']: this.selectedKey,
          ['campus']: this.selectedCampus}
      });

      this.$emit('update:selected', {id: this.selectedKey,
        campus: this.selectedCampus});
    },

    fetch_course_data(){
      const vue = this;
      this.axios.get("/api/v1/courses/" + this.selectedCampus).then((response) => {
        vue.courseList = response.data;
        this.loadingList = false;
      });
    },
    fetch_major_data(){
      const vue = this;
      this.axios.get("/api/v1/majors/" + this.selectedCampus).then((response) => {
        vue.majorList = response.data;
        this.loadingList = false;
      });
    },
    validateInput() {

      // get the value in the input
      let val = document.getElementById("searchInput").value;

      // get a list of option values from the datalist
      //let obj = document.getElementById("searchDataList").find("option[value='" + val + "']");

      alert(val);

      // check to make sure that 'val' is in the 'obj' datalist
      if(obj != null && obj.length > 0) {
          return this.isValidInput = true;
      }
      else {
          return this.isValidInput = false;
      }

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

</style>
