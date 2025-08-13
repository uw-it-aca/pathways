<template>
  <div>
    <h2 class="fs-6 fw-semibold fst-italic">{{ result_count }} results</h2>
  </div>
  <div class="container">
    <ul class="list-unstyled pt-3">
      <li v-for="result in displayed_results" :key="result.id">
        <template v-if="result.is_major">
          <div class="clearfix">
            <a :href="result.url" class="float-start">{{ result.title }}</a>
            <div
              class="badge text-bg-light rounded-pill text-uppercase float-end"
            >
              {{ result.campus }}
            </div>
          </div>
          <div class="small">{{ result.description }}</div>

          <!-- {{ result.abbr }} -->
          <!-- {{ result.description }} -->
        </template>
        <template v-if="result.is_course">
          <div class="clearfix">
            <a :href="result.url" class="float-start">
              <span class="text-decoration-none fw-semibold"
                >{{ result.id }}
              </span>
              {{ result.title }}</a
            >
            <div
              class="badge text-bg-light rounded-pill text-uppercase float-end"
            >
              {{ result.campus }}
            </div>
          </div>
          <div class="small">{{ result.description }}</div>
        </template>
      </li>
    </ul>
    <nav aria-label="Page navigation example">
      <ul class="pagination pagination-sm justify-content-center overflow-auto">
        <li class="page-item">
          <a
            class="page-link"
            href="#"
            aria-label="Previous"
            @click.prevent="goToPrevious"
          >
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li
          v-for="(pagenum, index) in page_numbers"
          :key="index"
          class="page-item"
        >
          <a
            class="page-link"
            :class="pagenum == page ? 'active' : ''"
            href="#"
            @click.prevent="goToPage(pagenum)"
            >{{ pagenum }}</a
          >
        </li>
        <li class="page-item">
          <a
            class="page-link"
            href="#"
            aria-label="Next"
            @click.prevent="goToNext"
          >
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script>
export default {
  name: "SearchResults",
  components: {},
  props: {
    searchResults: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      page: 1,
      pageSize: 30,
    };
  },
  computed: {
    result_count() {
      if (this.search_results === null) {
        return 0;
      } else {
        return this.search_results.length;
      }
    },
    displayed_results() {
      return this.search_results.slice(
        (this.page - 1) * this.pageSize,
        this.page * this.pageSize
      );
    },
    page_numbers() {
      return Array.from(
        { length: Math.ceil(this.result_count / this.pageSize) },
        (_, i) => i + 1
      );
    },
  },
  watch: {},
  methods: {
    goToPage(pagenum) {
      this.page = pagenum;
    },
    goToPrevious() {
      if (this.page > 1) {
        this.page -= 1;
      }
    },
    goToNext() {
      if (this.page < this.page_numbers.length) {
        this.page += 1;
      }
    },
  },
};
</script>
