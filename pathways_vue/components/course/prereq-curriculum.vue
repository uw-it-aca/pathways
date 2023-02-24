// prereq-curriculum.vue

<template>
  <div v-if="curricData === undefined" class="p-3">
    <div class="alert alert-purple" role="alert">
      <p>
        The curriculum {{ curric_id }} does not have courses with prerequisites.
      </p>
    </div>
  </div>
  <div class="mt-3" v-else>
    <prereq-curr-list :course-data="curricData.course_data" />
  </div>
</template>

<script>
import PrereqCurrList from "./prereq-curr-list.vue";

export default {
  name: "PrereqCurriculum",
  components: {
    "prereq-curr-list": PrereqCurrList,
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
      curricData: undefined,
    };
  },
  watch: {
    curric_id(newValue) {
      this.get_curric_prereqs(newValue);
    },
  },
  computed: {
    has_data: function () {
      return Object.keys(this.curricData).length > 0;
    },
  },
  mounted() {
    this.get_curric_prereqs(this.curric_id);
  },
  methods: {
    get_curric_prereqs(curric_id) {
      const vue = this;
      this.axios
        .get("/api/v1/curric_prereq/" + curric_id)
        .then((response) => {
          // don't show graph if there are no nodes/edges to display
          if (Object.keys(response.data.prereq_graph.x.edges.from).length > 0) {
            vue.curricData = response.data;
          }
        })
        .catch(function () {
          vue.curricData = {};
        });
    },
  },
};
</script>
