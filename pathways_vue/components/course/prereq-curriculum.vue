// prereq-curriculum.vue 

<template>
  <div class="p-3">
    <div class="form-check form-switch">
      <input 
        class="form-check-input" 
        type="checkbox" 
        v-model="viewCurrList" 
        id="ToggleCurrList" 
      />
      <label class="form-check-label" for="ToggleCurrList">View CHEM curriculum as a list</label>
    </div>
  </div>
  <prereq-curr-list v-if="viewCurrList" />
  <div class="card shadow-sm" id="ViewCurrMap" v-else>
    <div class="text-dark p-3 bg-light rounded-top rounded-sm">
      <small>Use the scroll function on your mouse or touchpad to zoom in and out</small>
    </div>
  </div>
</template>

<script>
import PrereqCurrList from './prereq-curr-list.vue';

export default {
  name: 'PrereqCurriculum',
  components: {
    'prereq-curr-list': PrereqCurrList,
  },
  data() {
    return { 
      viewCurrList: false, 
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>