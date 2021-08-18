// major.vue
<template>
  <div class="input-group">
    <input type="text" v-model="majorName" class="form-control" aria-label="" placeholder="Enter a major" list="majors" />
    <button type="button" class="btn btn-purple" @click="goToSelectedMajor">Search</button>
  </div>
  <datalist id="majors">
    <option v-for="(major, i) in majorList" :key="i">{{ major["Major"] }}</option>
  </datalist>
</template>

<script>

export default {
  name: "SearchMajor",
  props: {
    majorList: {
      type: Array,
      required: true,
    },
    selectedMajor: Object,
  },
  emits: ['update:selectedMajor'],
  data() {
    return {
      majorName: this.$route.query.name,
    };
  },
  mounted() {
    this.syncSelectedMajor();
  },
  methods: {
    syncSelectedMajor() {
      this.$emit(
        'update:selectedMajor',
        this.majorList.find((major) => major["Major"] == this.majorName),
      );
    },
    goToSelectedMajor() {
      this.$router.push({query: { name: this.majorName }});
      this.syncSelectedMajor();
    }
  }
};
</script>

<style lang="scss"></style>
