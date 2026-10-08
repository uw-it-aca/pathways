<template>
  <SHeading
    level="1"
    class="fw-bold ff-encode-sans mb-3"
    data-clarity-unmask="true"
    >{{ preventWidow(major.credential_title) }}</SHeading
  >
  <div class="mb-5">
    <p class="text-uppercase mb-1">
      {{ major["major_school"] }} - {{ major["major_campus"] }}
    </p>
    <p>
      <strong class="me-2">Admission Type:</strong>
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
  import { SHeading } from "solstice-vue";
  import { preventWidow } from "@/utils";

  export default {
    name: "MajorDetails",
    components: {
      SHeading,
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
    methods: {
      preventWidow,
    },
  };
</script>
