<template>
  <div class="my-2 py-2">
    <h6 class="fw-bold ff-open-sans mb-1">
      <a
        :href="major_url"
        class="text-decoration-none"
        style="color: #2f68cb"
        >{{ majorData.credential_title }}</a
      >
    </h6>
    <p class="text-uppercase small text-black-50 mb-0">
      {{ majorData.major_school }} - {{ majorData.campus }}
    </p>
    <!--
    <a
      href="/faq#admission_types"
      class="router-link-active text-capitalize"
      title="Admission to majors"
      ><major-capacity-display :admissionType="majorData.major_admission"
    /></a>-->
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
      return "/major?id=" + encodeURIComponent(this.majorData.id);
    },
  },
};
</script>
