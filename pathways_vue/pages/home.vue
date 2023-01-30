// home.vue
<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row justify-content-center">
        <div class="col-md-9">
          <h1 class="visually-hidden">{{ pageTitle }}</h1>

          <!-- Modal -->
          <div
            class="modal fade"
            role="dialog"
            id="exampleModal"
            tabindex="-1"
            aria-modal="true"
            aria-labelledby="welcome_modal"
            aria-hidden="true"
          >
            <div class="modal-dialog modal-dialog-centered modal-lg">
              <div class="modal-content">
                <div class="modal-body">
                  <h2 class="modal-title mb-2" id="welcome_modal">Welcome</h2>
                  <div>
                    <p>
                      DawgPath helps you discover courses and majors you're
                      enables you to be strategic when making decisions about
                      schedule. It provides useful data when planning to apply
                      selective screening. A few things to keep in mind before
                      getting started:
                    </p>
                    <ul>
                      <li>
                        Grades are just one of the factors considered for
                        capacity-constrained major. Reach out to your adviser to
                        learn more.
                      </li>
                      <li>
                        The median course grade and GPA data are only included
                        who had declared for the major.
                      </li>

                      <li>
                        Discovering and applying for a major can be a
                        challenging experience. Look for the "Find your adviser”
                        links to connect with your adviser.
                      </li>
                      <li>
                        Check out the <a href="/faq">DawgPath FAQ</a> for more
                        info.
                      </li>
                    </ul>
                  </div>
                  <div class="text-end">
                    <button
                      type="button"
                      class="btn btn-purple"
                      data-bs-dismiss="modal"
                      aria-label="Ok, got it"
                      @click="saveModalPref"
                    >
                      OK, got it
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <search-chooser />
          <!-- Button trigger modal -->
          <button
            type="button"
            class="btn btn-link mt-2 btn-sm text-decoration-none"
            aria-label="Open modal"
            @click="showWelcomeModal"
          >
            About DawgPath <i class="bi bi-info-circle"></i>
          </button>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import SearchChooser from "../components/search/chooser.vue";

import { Modal } from "bootstrap";

export default {
  name: "HomeComp",
  components: {
    layout: Layout,
    "search-chooser": SearchChooser,
  },
  data() {
    return {
      pageTitle: "Home",
      welcomeModal: null,
    };
  },
  mounted() {
    if (window.show_welcome) {
      // show the welcome modal when the component is mounted
      this.showWelcomeModal();
    }
  },
  methods: {
    showWelcomeModal() {
      this.welcomeModal = new Modal(
        document.getElementById("exampleModal"),
        {}
      );
      this.welcomeModal.show();
    },
    saveModalPref() {
      this.axios({
        method: "post",
        url: "/api/v1/user_pref/",
        headers: { "X-CSRFToken": window.csrf_token },
        data: {
          viewed_welcome_display: true,
        },
      });
    },
  },
};
</script>

<style lang="scss">
.modal-body li {
  margin-bottom: 1em;
}
</style>
