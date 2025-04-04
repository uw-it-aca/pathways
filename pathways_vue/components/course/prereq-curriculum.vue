// prereq-curriculum.vue

<template>
  <div v-if="curricData === undefined" class="p-3">
    <div class="alert alert-purple" role="alert">
      <p>
        The curriculum {{ curric_id }} does not have courses with prerequisites.
      </p>
    </div>
  </div>
  <div v-else class="mt-3">
    <prereq-curr-list :course-data="curricData.course_data" />
  </div>
</template>

<script>
import PrereqCurrList from "@/components/course/prereq-curr-list.vue";

export default {
  name: "PrereqCurriculum",
  components: {
    "prereq-curr-list": PrereqCurrList,
  },
  props: {
    curricId: {
      type: String,
      required: true,
    },
    courseId: {
      type: String,
      required: false,
      default: "",
    },
  },
  data() {
    return {
      viewCurrList: false,
      curricData: undefined,
    };
  },
  computed: {
    has_data: function () {
      return Object.keys(this.curricData).length > 0;
    },
  },
  watch: {
    curric_id(newValue) {
      this.get_curric_prereqs(newValue);
    },
  },
  mounted() {
    this.get_curric_prereqs(this.curric_id);
  },
  methods: {
    async get_curric_prereqs(curric_id) {
      const vue = this;

      try {
        const data = await useCustomFetch("/api/v1/curric_prereq/" + curric_id);

        // don't show graph if there are no nodes/edges to display
        if (Object.keys(data.prereq_graph.x.edges.from).length > 0) {
          vue.curricData = data;
        }
      } catch (error) {
        vue.curricData = {};
      }
    },
  },
};
</script>
