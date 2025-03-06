<template>
  <h3><a href="major_url">{{majorData.title}}</a></h3>
  <p>{{majorData.college}} - {{majorData.campus}}</p>
  <p>Admission Icon: {{majorData.admission}}</p>
  <a v-if="has_children" href="#" v-on:click.prevent="expandChildren">&gt;</a>
  <div v-if="expanded">
    <similar-major-row
      v-for="(major, index) in majorData.childMajors"
      :key="index"
      :majorData="major"
    />
  </div>
</template>

<script>

export default {
  name: "SimilarMajorRow",
  props: {
    majorData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      expanded: false
    };
  },
  methods: {
    expandChildren() {
      this.expanded = !this.expanded
    },
  },
  computed: {
    has_children() {
      return this.majorData.childMajors !== undefined && this.majorData.childMajors.length > 0
    },
  },
};
</script>
