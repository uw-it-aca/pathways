// major.vue

<template>
  <div class="input-group">
    <input type="text" class="form-control" aria-label="" placeholder="Enter a major" />
    <button type="button" class="btn btn-purple" @click="searchMajor">Search</button>
  </div>
</template>

<script>

export default {
  name: "SearchMajor",
  data() {
    return {};
  },
  methods: {
    searchMajor(event) {
      // TODO: wire up submit for major search
      alert('wire me up!')
    }
  }
};
</script>

<style lang="scss"></style>
