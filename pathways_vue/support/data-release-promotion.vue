<template>
  <div class="data-release-promotion">
    <div class="container-fluid py-4">
      <h1 class="mb-4">Data Release Promotion</h1>

      <!-- Error Alert -->
      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>Error:</strong> {{ error }}
        <button type="button" class="btn-close" @click="error = null"></button>
      </div>

      <!-- Success Alert -->
      <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
        {{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage = null"></button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading available releases...</p>
      </div>

      <!-- Main Content -->
      <div v-else class="row">
        <!-- Releases List -->
        <div class="col-lg-8">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Available Releases</h5>
            </div>
            <div class="card-body">
              <div v-if="releases.length === 0" class="alert alert-info">
                No data releases available.
              </div>
              <div v-else class="list-group">
                <button
                  v-for="release in releases"
                  :key="release.release_id"
                  type="button"
                  class="list-group-item list-group-item-action"
                  :class="{ active: selectedRelease?.release_id === release.release_id }"
                  @click="selectRelease(release)"
                >
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ release.release_id }}</h6>
                    <small class="text-muted">
                      {{ formatDate(release.updated) }}
                    </small>
                  </div>
                  <small class="text-muted d-block">
                    Manifest: {{ formatBytes(release.manifest_size) }}
                  </small>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Release Details -->
        <div class="col-lg-4">
          <div v-if="selectedRelease" class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Release Details</h5>
            </div>
            <div class="card-body">
              <dl class="row mb-3">
                <dt class="col-sm-5">Release ID:</dt>
                <dd class="col-sm-7">
                  <code>{{ selectedRelease.release_id }}</code>
                </dd>

                <dt class="col-sm-5">Updated:</dt>
                <dd class="col-sm-7">
                  {{ formatDate(selectedRelease.updated) }}
                </dd>

                <dt class="col-sm-5">Size:</dt>
                <dd class="col-sm-7">
                  {{ formatBytes(selectedRelease.manifest_size) }}
                </dd>
              </dl>

              <!-- Manifest Details -->
              <div v-if="manifestDetails" class="mb-3">
                <h6 class="mb-2">Manifest Information</h6>
                <small class="d-block text-muted">
                  Schema: {{ manifestDetails.schema_version }}
                </small>
                <small class="d-block text-muted">
                  Artifacts: {{ Object.keys(manifestDetails.artifacts || {}).length }}
                </small>
              </div>

              <!-- Artifacts List -->
              <div v-if="displayArtifacts && manifestDetails?.artifacts" class="mb-3">
                <h6 class="mb-2">Artifacts</h6>
                <ul class="list-unstyled small">
                  <li v-for="(artifact, name) in manifestDetails.artifacts" :key="name" class="mb-1">
                    <i class="bi bi-file"></i>
                    {{ name }}
                    <br>
                    <small class="text-muted d-block ps-3">
                      {{ formatBytes(artifact.size_bytes) }}
                      · SHA256: <code>{{ artifact.checksum_sha256.substring(0, 8) }}...</code>
                    </small>
                  </li>
                </ul>
              </div>

              <!-- Action Buttons -->
              <div class="d-grid gap-2">
                <button
                  type="button"
                  class="btn btn-primary"
                  :disabled="promoting || !selectedRelease"
                  @click="promoteRelease"
                >
                  <span v-if="promoting" class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Promoting...</span>
                  </span>
                  {{ promoting ? "Promoting..." : "Promote Release" }}
                </button>
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  :disabled="loadingManifest"
                  @click="refreshManifest"
                >
                  {{ loadingManifest ? "Loading..." : "Refresh Details" }}
                </button>
              </div>
            </div>
          </div>
          <div v-else class="card text-muted text-center py-5">
            <p>Select a release to view details</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataReleasePromotion",
  props: {
    tool: {
      type: Object,
      default: () => ({}),
    },
    links: {
      type: Array,
      default: () => [],
    },
    pageData: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      releases: [],
      selectedRelease: null,
      manifestDetails: null,
      loading: true,
      loadingManifest: false,
      promoting: false,
      error: null,
      successMessage: null,
      displayArtifacts: true,
    };
  },
  computed: {
    apiBaseUrl() {
      return "/api/v1/admin";
    },
  },
  mounted() {
    this.loadReleases();
  },
  methods: {
    async loadReleases() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`${this.apiBaseUrl}/releases/`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        if (data.success) {
          this.releases = data.releases || [];
        } else {
          this.error = data.error || "Failed to load releases";
        }
      } catch (err) {
        this.error = `Failed to load releases: ${err.message}`;
        console.error("Error loading releases:", err);
      } finally {
        this.loading = false;
      }
    },

    async selectRelease(release) {
      this.selectedRelease = release;
      await this.loadManifest(release.release_id);
    },

    async loadManifest(releaseId) {
      this.loadingManifest = true;
      this.error = null;
      try {
        const response = await fetch(`${this.apiBaseUrl}/releases/${releaseId}/manifest/`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        if (data.success) {
          this.manifestDetails = data.manifest;
        } else {
          this.error = data.error || "Failed to load manifest";
          this.manifestDetails = null;
        }
      } catch (err) {
        this.error = `Failed to load manifest: ${err.message}`;
        this.manifestDetails = null;
        console.error("Error loading manifest:", err);
      } finally {
        this.loadingManifest = false;
      }
    },

    async refreshManifest() {
      if (this.selectedRelease) {
        await this.loadManifest(this.selectedRelease.release_id);
      }
    },

    async promoteRelease() {
      if (!this.selectedRelease) {
        this.error = "No release selected";
        return;
      }

      if (!window.confirm(
        `Promote release "${this.selectedRelease.release_id}" for import? ` +
        "This will queue the data for import into the database."
      )) {
        return;
      }

      this.promoting = true;
      this.error = null;
      try {
        const response = await fetch(`${this.apiBaseUrl}/releases/promote/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.getCsrfToken(),
          },
          body: JSON.stringify({
            release_id: this.selectedRelease.release_id,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.error || `HTTP ${response.status}`);
        }

        const data = await response.json();
        if (data.success) {
          this.successMessage =
            `Release "${this.selectedRelease.release_id}" has been queued for import. ` +
            `Queue attempt: ${data.data.queue_attempt_id}`;
          // Refresh the releases list to show updated status
          setTimeout(() => this.loadReleases(), 1500);
        } else {
          this.error = data.error || "Failed to promote release";
        }
      } catch (err) {
        this.error = `Failed to promote release: ${err.message}`;
        console.error("Error promoting release:", err);
      } finally {
        this.promoting = false;
      }
    },

    getCsrfToken() {
      const name = "csrftoken";
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach((c) => {
          c = c.trim();
          if (c.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(c.substring(name.length + 1));
          }
        });
      }
      return cookieValue || "";
    },

    formatDate(dateString) {
      if (!dateString) return "Unknown";
      try {
        return new Date(dateString).toLocaleString();
      } catch {
        return dateString;
      }
    },

    formatBytes(bytes) {
      if (typeof bytes !== "number" || bytes === 0) return "0 B";
      const k = 1024;
      const sizes = ["B", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },
  },
};
</script>

<style scoped>
.data-release-promotion {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.list-group-item {
  border-color: #dee2e6;
  transition: all 0.2s ease;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  border-color: #0d6efd;
}

.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.card {
  border: 1px solid #dee2e6;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

code {
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
