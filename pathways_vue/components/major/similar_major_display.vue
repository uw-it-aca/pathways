<template>
  <h3><a :href="major_url">{{majorData.credential_title}}</a></h3>
  <p>{{majorData.major_school}} - {{majorData.campus}}</p>
  <major-capacity-display :admissionType="majorData.major_admission" />
</template>

<script>

import MajorCapacityDisplay from "@/components/major/capacity-display.vue";

export default {
  name: "SimilarMajorDisplay",
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
    return {};
  },
  methods: {},
  computed: {
    major_url() {
      return "/major?id=" + encodeURIComponent(this.majorData.id)
    }
  },
};
</script>
