// prereq-curriculum.vue

<template>
  <div class="p-3">
    <div class="form-check form-switch">
      <input
        class="form-check-input"
        type="checkbox"
        v-model="viewCurrList"
        id="ToggleCurrList"
      />
      <label class="form-check-label" for="ToggleCurrList">View {{curric_id}} curriculum as a list</label>
    </div>
  </div>
  <prereq-curr-list v-if="viewCurrList" />
  <div class="card shadow-sm" id="ViewCurrMap" v-else>
    <prereq-graph
      :v-if="has_data"
      :graph_data="curricData"
      graph_type="curric"
    />
    <div class="text-dark p-3 bg-light rounded-top rounded-sm">
      <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
    </div>
  </div>
</template>

<script>
import PrereqCurrList from './prereq-curr-list.vue';
import PrereqGraph from './prereq-graph.vue';

export default {
  name: 'PrereqCurriculum',
  components: {
    PrereqGraph,
    'prereq-curr-list': PrereqCurrList,
  },
  props: {
    curric_id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      viewCurrList: false,
      curricData: {}
    };
  },
  // mounted() {
  //   console.log('load curric prereq');
  //   this.get_curric_prereqs(this.curric_id);
  // },
  watch: {
    curric_id(newValue) {
      this.get_curric_prereqs(newValue);
    }
  },
  computed: {
    has_data: function (){
      return Object.keys(this.curricData).length > 0;
    }
  },
  methods: {
    get_curric_prereqs(curric_id){
      const vue = this;
      this.axios.get("/api/v1/curric_prereq/" + curric_id).then((response) => {
        vue.curricData = response.data;
      });
    }
  },
};
</script>

<style lang="scss"></style>
