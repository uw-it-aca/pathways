// lighthouserc.cjs
require("dotenv").config();
const port = process.env.RUNSERVER_PORT;

module.exports = {
  ci: {
    collect: {
      settings: {
        //set which categories you want to run
        onlyCategories: ["accessibility"],
      },
      url: [
        // add URLs to be tested (usually matches /pages structure)
        `http://localhost:${port}/`,
        `http://localhost:${port}/faq`,
        `http://localhost:${port}/major?id=C%20SCI-0-1-5`,
        `http://localhost:${port}/course?id=CSE%20142`,
      ],
      // specify other options like numberOfRuns, staticDistDir, etc.
      numberOfRuns: 1,
    },
    // add assert, upload, and other configuration as required
    assert: {},
    upload: {},
    server: {},
    wizard: {},
  },
};
