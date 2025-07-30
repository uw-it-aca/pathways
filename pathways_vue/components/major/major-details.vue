<template>
  <div class="mb-5">
    <h1 class="h2 axdd-font-encode-sans fw-bold">
      {{ major["credential_title"] }}
    </h1>
    <p class="text-uppercase mb-1">
      {{ major["major_school"] }} - {{ major["major_campus"] }}
    </p>
    <p>
      <strong class="me-2">Admission Policy:</strong>
      <a
        href="/faq#admission_types"
        class="router-link-active text-capitalize"
        title="Admission to majors"
        ><major-capacity-display :admissionType="this.major.major_admission"
      /></a>
    </p>
    <div class="major-info">
      <div class="major-description">
        <p v-html="major['credential_description']" />
      </div>
    </div>
  </div>
</template>

<script>
import MajorCapacityDisplay from "@/components/major/capacity-display.vue";

export default {
  name: "MajorDetails",
  components: {
    MajorCapacityDisplay,
  },
  props: {
    major: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
