// major.vue
<template>
  <search 
    inner-id="majors"
    :options="majorListSearchable"
    placeholder="Enter a major"
    route-path="major"
    sync-query-param="name"
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
    majorList: {
      type: Array,
      required: true,
    },
    selected: Object,
  },
  emits: ['update:selected'],
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
