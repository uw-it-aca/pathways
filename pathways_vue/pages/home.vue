// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>

      <div class="align-center mb-5"><i class="bi-alarm text-danger"></i> here is my clock icon</div>

      <!-- Button trigger modal -->
      <button
        type="button"
        class="btn btn-primary mb-5"
        data-bs-toggle="modal"
        data-bs-target="#exampleModal"
      >
        Launch demo modal
      </button>

      <!-- Modal -->
      <div
        class="modal fade"
        id="exampleModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-body">
              <h2 class="modal-title" id="exampleModalLabel">Modal title</h2>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>

              <div>asdfasdfasdf</div>

              <button type="button" class="btn btn-purple" data-bs-dismiss="modal">
                OK, got it
              </button>
            </div>
          </div>
        </div>
      </div>

      <ul>
        <li><router-link to="/major">Go to Major</router-link></li>
        <li><router-link to="/course">Go to Course</router-link></li>
      </ul>

      <search-chooser />

    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import SearchChooser from '../components/search/chooser.vue';

import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';

export default {
  components: {
    'layout': Layout,
    'search-chooser': SearchChooser
  },
  data() {
    return {
      pageTitle: 'Home',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
