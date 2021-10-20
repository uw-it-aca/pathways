// course.vue
<template>
  <search
    inner-id="courses"
    :options="course_list"
    placeholder="Enter a course code"
    route-path="course"
    sync-query-param="code"
    v-model:selected="selected"
    :data-loading="is_loading"
  />
</template>

<script>
import Search from './search.vue';

export default {
  name: 'SearchCourse',
  components: {
    'search': Search,
  },
  props: {
    selected: String,
  },
  data() {
    return {
      course_list: [],
      is_loading: false
    };
  },
  emits: ['update:selected'],
  mounted() {
    const vue = this;
    this.is_loading = true;
    this.axios.get("/api/v1/courses/").then((response) => {
      vue.course_list = response.data;
      vue.is_loading = false;
    });
  },
  watch: {
    selected(newValue) {
      this.$emit('update:selected', newValue);
    }
  },
};
</script>

<style lang="scss"></style>
