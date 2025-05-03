<template>
  <div v-if="is_program">
    <a href="#" v-on:click.prevent="expandChildren">
      <h3><i :class="expand_icon"></i>{{majorData.program_title}}</h3>
    </a>
    <p>{{majorData.program_school}} - {{majorData.program_campus}}</p>
    <div v-if="expanded" style="margin-left: 40px;">
      <similar-major-display
        v-for="(major, index) in majorData.program_majors"
        :key="index"
        :majorData="major"
      />
    </div>
  </div>
  <div v-else>
    <similar-major-display :major-data="majorData" />
  </div>
<!--  <h3><a :href="major_url">{{majorData.credential_title}}</a></h3>-->
<!--  <p>{{majorData.major_school}} - {{majorData.campus}}</p>-->
<!--  <major-capacity-display :admissionType="majorData.major_admission" />-->

</template>

<script>

import SimilarMajorDisplay from "./similar_major_display.vue";

export default {
  name: "SimilarMajorRow",
  components: {
    SimilarMajorDisplay,
  },
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
    major_url() {
      return "/major?id=" + encodeURIComponent(this.majorData.id)
    },
    is_program() {
      return this.majorData.program_majors !== undefined;
    },
    expand_icon() {
      return this.expanded ? "bi-chevron-compact-up" : "bi-chevron-compact-down"
    }
  },
};
</script>
