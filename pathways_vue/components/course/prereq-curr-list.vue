// prereq-curr-list.

<template>
  <p class="fw-bold">
    NOTE: This is an overview of every course in the CHEM department. For information on majors,
    please search for a major using the main search function.
  </p>
  <ul class="list-unstyled">
    <li class="mb-3">
      <div class="card shadow-sm">
        <div class="card-body p-3">
          <strong
            ><a href="/course/?code=ANTH+215" class="d-block mb-3">
              ANTH 215: Introduction to Medical Anthropology and Global Health</a
            ></strong
          >
          <div>
            <div class="container">
              <div class="row">
                <div class="p-0 mb-3 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Prerequisites</strong>
                      <span class="badge rounded-pill bg-purple">0</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <div><small>This course has no prerequisites.</small></div>
                </div>
                <div class="p-0 col-sm-6">
                  <div>
                    <small
                      ><strong class="text-dark">Available upon completion</strong>
                      <span class="badge rounded-pill bg-purple">3</span
                      ><span class="visually-hidden">courses</span></small
                    >
                  </div>
                  <ul class="prereq-list">
                    <li>
                      <a href="/course/?code=ANTH+303" class="active-router-link"><span class="badge bg-link-color text-light"
                        >ANTH 303</span></a
                      >
                    </li>
                    <li>
                      <a href="/course/?code=ANTH+422" class="active-router-link"><span class="badge bg-link-color text-light"
                        >ANTH 422</span></a
                      >
                    </li>
                    <li>
                      <a href="/course/?code=BIO+A+420" class="active-router-link"><span class="badge bg-link-color text-light"
                        >BIO A 420</span></a
                      >
                    </li>
                    <!---->
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'PrereqCurrList',
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.prereq-list {
  list-style: none;
  padding: 0;
}

.prereq-list li {
  display: inline-block;
  margin-right: 5px;
}

.prereq-list li:last-child a::after {
  content: '';
}

.rounded-pill {
  font-size: 75%;
  margin-left: 0.3rem;
}
</style>