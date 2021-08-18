// major-details.vue

<template>
  <div class="mb-5">
    <h2> {{ major["Major"] }}</h2>
    <p class="text-uppercase mb-1">{{ major["college"] }} - {{ major["campus"] }}</p>
    <p><strong>Admission Policy:</strong> {{ major["Admission Policy"] }}</p>
    <div class="major-info">
      <div class="major-description">
        <p v-html="major['Description']" />
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'MajorDetails',
  props: {
    major: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss"></style>
