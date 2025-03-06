<template>
  <h3><a :href="major_url">{{majorData.title}}</a></h3>
  <p>{{majorData.college}} - {{majorData.campus}}</p>
  <major-capacity-display :admissionType="majorData.admission" />
  <a v-if="has_children" href="#" v-on:click.prevent="expandChildren"><i :class="expand_icon"></i></a>
  <div v-if="expanded" style="margin-left: 40px;">
    <similar-major-row
      v-for="(major, index) in majorData.childMajors"
      :key="index"
      :majorData="major"
    />
  </div>
</template>

<script>

import MajorCapacityDisplay from "@/components/major/capacity-display.vue";

export default {
  name: "SimilarMajorRow",
  components: {
    MajorCapacityDisplay,
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
    has_children() {
      return this.majorData.childMajors !== undefined && this.majorData.childMajors.length > 0
    },
    expand_icon() {
      return this.expanded ? "bi-chevron-compact-up" : "bi-chevron-compact-down"
    }
  },
};
</script>
