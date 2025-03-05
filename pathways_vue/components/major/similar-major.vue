<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">Similar Majors</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "SimilarMajor",
  props: {
    similarMajorData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {},
  computed: {},
};
</script>
