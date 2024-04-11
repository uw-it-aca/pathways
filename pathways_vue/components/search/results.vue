<template>
  <div>
    <h2>Results - {{ result_count }}</h2>
    <ul>
      <li v-for="result in search_results" :key="result.id">
        {{ result.score }} - {{ result.contents }} <strong>({{result.campus}})</strong>
      </li>
    </ul>
  </div>
</template>
<script>

export default {
  name: 'Results',
  components: {
  },
  props: {
    search_results: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
    };
  },
  computed: {
    result_count() {
      if (this.search_results === null) {
        return 0;
      } else {
        return this.search_results.length;
      }
    },
  },
  watch: {
  },
  methods: {
  },
};
</script>

<style lang="scss">

</style>
