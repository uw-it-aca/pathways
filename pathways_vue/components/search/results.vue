<template>
  <div>
    <h2>Results - {{ result_count }}</h2>
    <ul class="list-group">
      <li
        class="list-group-item d-flex justify-content-between align-items-start border border-0"
        v-for="result in displayed_results"
        :key="result.id"
      >
        <div class="ms-2 me-auto">
          <a v-bind:href="result.url"
            >{{ result.score }} - {{ result.contents }}</a
          >
        </div>
        <span class="badge text-bg-light rounded-pill text-uppercase">{{
          result.campus
        }}</span>
      </li>
    </ul>
    <nav aria-label="Page navigation example">
      <ul class="pagination justify-content-center">
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
        <li v-for="pagenum in page_numbers" class="page-item">
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
  name: "Results",
  components: {},
  props: {
    search_results: {
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
