// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>{{ pageTitle }}</template>
    <template #content>
      <div class="row justify-content-center">
        <div class="col-md-9">
          <h1 class="visually-hidden">Pathways Home</h1>

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
                  <h2 class="modal-title mb-2" id="exampleModalLabel">Welcome</h2>
                  <div>
                    <p>
                      This app helps with course planning and preparation for applying to a major. A
                      few things to keep in mind before getting started:
                    </p>
                    <ul>
                      <li>
                        Grades are just one of the factors considered for admission to a
                        capacity-constrained major. Reach out to your adviser to learn more.
                      </li>

                      <li>
                        The median course grade and GPA data are only included for those students
                        who had declared for the major (median grade for Chem 142, only includes
                        those who declared Chemistry as their major).
                      </li>

                      <li>
                        Discovering and applying for a major can be a challenging experience. Look
                        for the “Contact your adviser” link to connect with your adviser.
                      </li>
                    </ul>
                  </div>
                  <div class="text-end">
                    <button
                      type="button"
                      class="btn btn-purple"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    >
                      OK, got it
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <ul>
            <li><router-link to="/major">Go to Major</router-link></li>
            <li><router-link to="/course">Go to Course</router-link></li>
          </ul>

          <search-chooser />
          <!-- Button trigger modal -->
          <button
            type="button"
            class="btn btn-link mb-5"
            @click="showWelcomeModal"
          >
            About this app
          </button>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';
import SearchChooser from '../components/search/chooser.vue';

import D3Arc from '../components/d3-arc.vue';
import D3BoxPlot from '../components/d3-boxplot.vue';

import { Modal } from 'bootstrap';

export default {
  components: {
    layout: Layout,
    'search-chooser': SearchChooser,
  },
  data() {
    return {
      pageTitle: 'Home',
      welcomeModal: null
    };
  },
  mounted() {
    // show the welcome modal when the component is mounted
    this.showWelcomeModal();
  },
  methods: {
    showWelcomeModal(event){
        this.welcomeModal = new Modal(document.getElementById('exampleModal'), {})
        this.welcomeModal.show()
    },
  },
};
</script>

<style lang="scss">
  .modal-body li {
    margin-bottom:1em;
  }
</style>
