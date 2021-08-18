<template>
  <div class="input-group">
    <input
      type="text"
      v-model="selectedLabel"
      class="form-control"
      aria-label=""
      :placeholder="placeholder"
      :list="innerId"
    />
    <button type="button" class="btn btn-purple" @click="onSelected">Search</button>
  </div>
  <datalist :id="innerId">
    <option v-for="(option, i) in renderableOptions" :key="i">{{ option }}</option>
  </datalist>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    innerId: {
      type: String,
      required: true,
    },
    options: {
      type: Object,
      required: true,
    },
    placeholder: {
      type: String,
      default: '',
    },
    routePath: {
      type: String,
      default: null,
    },
    syncQueryParam: {
      default: null,
      type: String,
    },
    selected: {},
  },
  emits: ['update:selected'],
  data() {
    return {
      selectedLabel: '',
    };
  },
  mounted() {
    if (this.syncQueryParam && this.$route.query[this.syncQueryParam]) {
      this.selectedLabel = this.options[
        decodeURIComponent(this.$route.query[this.syncQueryParam])
      ]?.label ?? '';
      this.syncSelected();
    }
  },
  methods: {
    syncSelected() {
      this.$emit('update:selected', this.options[this.selectedKey]?.data ?? '');
    },
    onSelected() {
      if (this.syncQueryParam) {
        this.$router.push({
          path: this.routePath,
          query: { [this.syncQueryParam]: encodeURIComponent(this.selectedKey) }
        });
      }
      this.syncSelected();
    },
    labelToKey(label) {
      let keyArr = Object.entries(this.options)
        .find(([_, value]) => value.label == label);
      return keyArr[0];
    },
  },
  computed: {
    renderableOptions() {
      return Object.entries(this.options).map(([_, value]) => value.label);
    },
    selectedKey() {
      let keyArr = Object.entries(this.options)
        .find(([_, value]) => value.label == this.selectedLabel) ?? [''];
      return keyArr[0];
    }
  },
};
</script>

<style lang="scss"></style>
