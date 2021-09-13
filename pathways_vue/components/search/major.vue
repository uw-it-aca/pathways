// major.vue
<template>
  <search
    inner-id="majors"
    :options="major_list"
    placeholder="Enter a major"
    route-path="major"
    sync-query-param="id"
    v-model:selected="selected"
  />
</template>

<script>
import Search from './search.vue';

export default {
  name: "SearchMajor",
  components: {
    'search': Search,
  },
  props: {
    selected: Object,
    prefill_id: ""
  },
  data() {
    return {
      major_list: []
    };
  },
  emits: ['update:selected'],
  mounted() {
    const vue = this;
    this.axios.get("/api/v1/majors/").then((response) => {
      vue.major_list = response.data;
    });
  },
  computed: {
    majorListSearchable() {
      let selectable = {};

      this.majorList.forEach((major) => {
        selectable[major["Major"].trim()] = {
          label: major["Major"].trim(),
          data: major,
        };
      });

      return selectable;
    }
  },
  watch: {
    selected(newValue) {
      this.$emit('update:selected', newValue);
    }
  },
};
</script>

<style lang="scss"></style>
