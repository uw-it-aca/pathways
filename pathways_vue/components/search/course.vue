// course.vue

<template>
  <div class="card bg-light mt-5">
    <div class="card-body">
      <h2 class="fw-bold mt-2 fs-5">Search for a course</h2>
      <form @submit.prevent="onSelected" role="search">
        <label for="text_search">Search:</label>
        <input id="text_search" v-model="form_data.search_string">
        <fieldset>
          <legend>Campus</legend>
          <input type="radio" id="seattle" value="seattle" v-model="form_data.campus" />
          <label for="seattle">Seattle</label>
          <input type="radio" id="bothell" value="bothell" v-model="form_data.campus" />
          <label for="bothell">Bothell</label>
          <input type="radio" id="tacoma" value="tacoma" v-model="form_data.campus" />
          <label for="tacoma">Tacoma</label>
        </fieldset>
        <input type="checkbox" id="gateway" v-model="form_data.is_gateway" />
        <label for="gateway">Gateway Course</label>
        <br />
        <input type="checkbox" id="bottleneck" v-model="form_data.is_bottleneck" />
        <label for="bottleneck">Bottleneck Course</label>
        <div class="coi-slider-container">
          <MultiRangeSlider
            id="coi-slider"
            class="coi-range-slider"
            :min="0"
            :max="5"
            :step="1"
            :ruler="false"
            :label="true"
            :minValue="0"
            :maxValue="5"
            @input="updateValues"
          />
        </div>
        <button type="submit" @click="runSearch">Search</button>
      </form>
    </div>
  </div>
</template>
<script>
import MultiRangeSlider from "multi-range-slider-vue";
import qs from "qs";

export default {
  name: 'CourseSearch',
  components: {
    MultiRangeSlider
  },
  props: {
  },
  data() {
    return {
      form_data: {
        search_string: "",
        campus: "",
        is_gateway: null,
        is_bottleneck: null,
        min_coi_score: 0,
        max_coi_score: 5,
      }
    };
  },
  computed: {
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
      this.axios.get("api/v1/course_search/", {
        params: vue.form_data,
        paramsSerializer: params => {
          return qs.stringify(params, {skipNulls: true})
        }
      }).then((response) => {
        console.log(response.data)
        // vue.majorList = response.data;
        // this.loadingList = false;
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
