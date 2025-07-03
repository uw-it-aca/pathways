<template>
  <div class="my-1 py-2" style="font-family: 'Open Sans';">
    <h3 class="fw-bold" style="font-size: 16px;">
    <a :href="major_url" class="text-decoration-none" style="color: #2f68cb;">{{majorData.credential_title}}</a>
    </h3>
    <p class="text-uppercase text-secondary mb-1" style="font-size: 14px;">{{majorData.major_school}} - {{majorData.campus}}
    </p>
    <major-capacity-display :admissionType="majorData.major_admission" />
  </div>
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
