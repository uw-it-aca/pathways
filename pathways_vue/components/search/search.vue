<template>
  <div class="input-group">
    <input
      type="text"
      v-model="selectedLabel"
      class="form-control"
      aria-label=""
      :placeholder="placeholder"
      :list="innerId"
    />q
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
      this.selectedLabel = this.options[this.$route.query[this.syncQueryParam]]?.label ?? '';
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
          query: { [this.syncQueryParam]: this.selectedKey }
        });
      }
      this.syncSelected();
    }
  },
  computed: {
    renderableOptions() {
      return this.options.map(m => m.value)
    },
    selectedKey() {
      let selectedObj = this.options.find(o => o.value === this.selectedLabel);
      if (selectedObj !== undefined){
        return selectedObj.key;
      }
    }
  },
};
</script>

<style lang="scss"></style>
