// Copyright 2026 UW-IT, University of Washington
// SPDX-License-Identifier: Apache-2.0

/**
 * SPA entry point for data release promotion tool
 * Registers with the supporttools framework for use in django-supporttools
 */

window.supporttoolsRegisterSpaTool(
  "data_release_promotion",
  () => import("./data-release-promotion.vue")
);
