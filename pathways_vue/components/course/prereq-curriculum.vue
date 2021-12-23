// prereq-curriculum.vue

<template>
  <div v-if="curricData === undefined" class="p-3">
    <div class="alert alert-info" role="alert">
      <p>The curriculum {{curric_id}} did not display a graph. Here are some possible reasons:</p>
        <ul>
          <li>The curriculum code does not exist</li>
          <li>The map does not display graduate curriculum</li>
          <li>The curriculum does not have courses with prerequisites</li>
        </ul>
    </div>
  </div>
  <div v-else>
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
    <prereq-curr-list
      v-if="viewCurrList"
      :course-data="curricData.course_data"
    />
    <div class="card shadow-sm" id="ViewCurrMap" v-else>
      <prereq-graph
        :v-if="has_data"
        :graph_data="curricData.prereq_graph"
        graph_type="curric"
        :active_course="course_id"
      />
      <div class="text-dark p-3 bg-light rounded-top rounded-sm">
        <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
      </div>
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
    course_id: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      viewCurrList: false,
      curricData: undefined
    };
  },
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
  mounted() {
    this.get_curric_prereqs(this.curric_id);
  },
  methods: {
    get_curric_prereqs(curric_id){
      const vue = this;
      this.axios.get("/api/v1/curric_prereq/" + curric_id).then((response) => {
        // don't show graph if there are no nodes/edges to display
        if(Object.keys(response.data.prereq_graph.x.edges.from).length > 0){
          vue.curricData = response.data;
        }
      }).catch(function (error) {
        vue.curricData = {};
      });
    }
  },
};
</script>

<style lang="scss"></style>
