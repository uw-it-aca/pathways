// major.vue
<template>
  <div class="input-group">
    <input type="text" class="form-control" aria-label="" placeholder="Enter a major" list="majors" />
    <button type="button" class="btn btn-purple" @click="searchMajor">Search</button>
  </div>
  <datalist id="majors">
    <option>American Ethnic Studies</option>
    <option>Anthropology</option>
    <option>Applied Mathematics</option>
    <option>Communication</option>
    <option>Economics</option>
    <option>Philosophy</option>
    <option>Physics</option>
    <option>Bioresource Science &amp; Engineering</option>
    <option>Computer Engineering</option>
    <option>Environmental Health</option>
    <option>Social Welfare</option>
  </datalist>
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
