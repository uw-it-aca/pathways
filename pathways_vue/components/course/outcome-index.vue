// outcome-index.vue

<template>
  <div class="card mb-5">
    <div class="card-body">
      <h2 class="h4 axdd-font-encode-sans fw-bold">
        Course Outcome Index (COI)
        <small class="align-top"
          ><span class="h2 badge text-bg-info">BETA</span></small
        >
      </h2>
      <p>
        The COI score is calculated by using a new model to predict how well
        students will do in a class, then comparing the predictions with actual
        course outcomes.
        <a
          type="button"
          class="btn-link text-decoration-none"
          aria-label="Open modal"
          @click="showCOIModal"
        >
          Walk me through the COI <i class="bi bi-info-circle"></i>
        </a>
      </p>
      <div
        class="modal fade"
        role="dialog"
        id="coi_modal"
        tabindex="-1"
        aria-modal="true"
        aria-labelledby="coi_onboard"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-body">
              <div>
                <div id="coi_onboard_steps" class="carousel slide">
                  <div class="carousel-indicators mb-0">
                    <button
                      type="button"
                      data-bs-target="#coi_onboard_steps"
                      data-bs-slide-to="0"
                      class="bg-purple active"
                      aria-current="true"
                      aria-label="Slide 1"
                    ></button>
                    <button
                      type="button"
                      data-bs-target="#coi_onboard_steps"
                      data-bs-slide-to="1"
                      class="bg-purple"
                      aria-label="Slide 2"
                    ></button>
                    <button
                      type="button"
                      data-bs-target="#coi_onboard_steps"
                      data-bs-slide-to="2"
                      class="bg-purple"
                      aria-label="Slide 3"
                    ></button>
                  </div>
                  <div class="carousel-inner">
                    <div class="carousel-item active">
                      <img
                        src="/pathways/static/pathways/img/modal-1-scale.png"
                        class="d-block w-100"
                        alt="alt text"
                      />
                      <div class="carousel-caption d-none d-md-block">
                        <h5>As a student, why should I care about COI?</h5>
                        <p class="text-start">
                          The COI provides insight into how challenging a course
                          may be. Lower numbers indicate that the class had
                          fewer students earning credit than predicted. Numbers
                          in the middle of the scale indicate a course that is
                          typical at the UW. Positive numbers indicate that the
                          class had more students earning credit than predicted.
                        </p>
                      </div>
                    </div>
                    <div class="carousel-item">
                      <img
                        src="/pathways/static/pathways/img/modal-2-scale.png"
                        class="d-block w-100"
                        alt="alt text"
                      />
                      <div class="carousel-caption d-none d-md-block">
                        <h5>
                          Concerned that your schedule may be too challenging?
                        </h5>
                        <p class="text-start">
                          Some students do poorly in a quarter or drop courses
                          as a result of taking too many difficult courses in
                          the same quarter.
                          <strong
                            >If feasible, try to keep a good balance of negative
                            and positive COI scores each quarter.</strong
                          >
                          If you're concerned about your potential course load,
                          reach out to an adviser.
                        </p>
                      </div>
                    </div>
                    <div class="carousel-item">
                      <img
                        src="/pathways/static/pathways/img/modal-3-scale.png"
                        class="d-block w-100"
                        alt="alt text"
                      />
                      <div class="carousel-caption d-none d-md-block">
                        <h5>How is the number in the scale calculated?</h5>
                        <p class="text-start">
                          The COI score is calculated by using a model to
                          predict how well students will do in a class, then
                          comparing the predictions with actual grade outcomes.
                          <strong
                            >Keep in mind that this score is just a prediction
                            and may not be your actual experience.</strong
                          >
                          Explore how the course compares to other classes in
                          that major, and other majors at the UW.
                        </p>
                      </div>
                    </div>
                  </div>
                  <button
                    class="carousel-control-prev"
                    type="button"
                    data-bs-target="#coi_onboard_steps"
                    data-bs-slide="prev"
                  >
                    <span
                      class="carousel-control-prev-icon bg-purple"
                      aria-hidden="true"
                    ></span>
                    <span class="visually-hidden">Previous</span>
                  </button>
                  <button
                    class="carousel-control-next"
                    type="button"
                    data-bs-target="#coi_onboard_steps"
                    data-bs-slide="next"
                  >
                    <span
                      class="carousel-control-next-icon bg-purple"
                      aria-hidden="true"
                    ></span>
                    <span class="visually-hidden">Next</span>
                  </button>
                </div>
              </div>
              <div class="text-end">
                <button
                  type="button"
                  class="btn btn-purple"
                  data-bs-dismiss="modal"
                  aria-label="Next"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-light" v-if="course_coi == null">
        <div class="alert alert-purple" role="alert">
          <p>
            The COI is not available for
            <strong>{{ course.course_id }}</strong> because there isn't enough
            data for this course.
          </p>
        </div>
      </div>
      <div class="bg-light" v-else>
        <div id="sr-text" class="screen-reader-only"></div>
        <div
          id="upper"
          class="d-flex justify-content-between align-items-start"
        >
          <div class="card coi-score text-bg-gold text-center">
            <span class="fw-bold">{{ course.course_id }}</span>
            <div id="score"></div>
          </div>
          <div id="layer-select" class="card"></div>
        </div>
        <div aria-hidden="true" id="coiGraph" />
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { Modal } from "bootstrap";
import { select } from "d3";

export default {
  name: "OutcomeScore",
  data() {
    return {
      percent_in_range: null,
      course_coi: null,
      course_level_coi: null,
      curric_coi: null,
      curric_id: null,
      curric_abbr: null,
      course_num: null,
      course_level: null,
      course_coi_data: null,
      curric_coi_data: null,
    };
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  watch: {
    course: function (course) {
      this.init();
    },
  },
  mounted() {
    //var popover = new Popover(document.querySelector(".info-popper"));
    this.init();
  },
  computed: {},
  methods: {
    showCOIModal() {
      this.coiModal = new Modal(document.getElementById("coi_modal"), {});
      this.coiModal.show();
    },
    init() {
      this.percent_in_range = this.course.coi_data.percent_in_range;
      this.course_coi = this.course.coi_data.course_coi;
      this.course_level_coi = this.course.coi_data.course_level_coi;
      this.curric_coi = this.course.coi_data.curric_coi;
      this.course_id = this.course.course_id;

      var split_pos = this.course_id.lastIndexOf(" ");
      this.curric_abbr = this.course_id.substring(0, split_pos);
      this.course_num = parseInt(
        this.course_id.substring(split_pos + 1, this.course_id.length)
      );
      this.course_level = Math.floor(this.course_num / 100) * 100;

      if (this.course_coi != null) {
        this.getCourseCOI();
      }
    },
    getData() {
      this.getCurricCOI();
    },

    generateRect() {
      let vue = this;
      // Store chosen course
      var chosenCourse;
      // Store chosen major
      var chosenMajor;

      // Clear any previous graphs
      document.getElementById("coiGraph").innerHTML = "";
      const margin = { top: 20, right: 10, bottom: 20, left: 10 };
      const width = 600 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom,
        rwidth = width + margin.left + margin.right,
        rheight = height + margin.top + margin.bottom;

      // Append SVG to container
      const svg = d3
        .select("#coiGraph")
        .append("svg")
        .attr("viewBox", `0 0 ${rwidth} ${rheight}`)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Tooltip for hover
      const tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("color", "#000")
        .style("background-color", "#eaeaea")
        .style("width", "auto")
        .style("opacity", 0)
        .style("left", "-9999px")
        .style("visibility", "hidden");

      // Pull in data to plot on line
      const coursePicked = vue.course_id;
      // Get the major of the chosen course
      const majorPicked = coursePicked.match(/\D+/)[0].trim();
      // Specify ID of course
      var courseId = "#" + coursePicked.replace(/\s/g, "_");

      // Specific course color (gold)
      const courseColor = "#ffbc24";
      // Major course color (teal)
      const majorColor = "#4c7286";
      // Major averages (purple)
      const avgColor = "#452a78";

      // Different layer options
      const layerOptions = {
        single: {
          name: coursePicked,
          color: courseColor,
        },
        chosen: {
          name: "All " + majorPicked + " Courses",
          color: majorColor,
        },
        other: {
          name: "Other Major Averages",
          color: avgColor,
        },
      };

      // Set radius here
      const RADIUS = 4.2;
      // Where the points will hover around vertically
      const yCenter = 65;

      // Create the 5.0 COI scale
      const x = d3.scaleLinear().domain([-5, 5]).range([0, width]);

      // Scale score from -5 to 5
      // var scaleScore = d3.scaleLinear().domain([0, 5]).range([5, -5]);

      // Draw the axis
      var xAxis = d3.axisBottom(x).ticks(11);

      // Add axis to the svg
      svg
        .append("g")
        .attr("class", "x axis")
        .attr(
          "transform",
          "translate(0," + (height - margin.bottom * 0.3) + ")"
        )
        .call(
          xAxis
            .tickValues([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
            .tickFormat(function (d) {
              return d3.format(".0f")(d);
            })
        );

      // Where the layer select buttons will be
      var layerSelect = d3.select("#layer-select");

      // Clear legend so new data can be added
      layerSelect.html("");

      // Add some text to the container
      layerSelect
        .append("p")
        .text("View " + coursePicked + " in context")
        .style("font-weight", "bold");

      var selectID;

      // Add the two options as radio buttons
      for (var option in layerOptions) {
        selectID = layerOptions[option].name.replace(" ", "-");

        var inputRow = layerSelect.append("div").attr("class", "form-check");

        // Add the radio buttons
        inputRow
          .append("input")
          .attr("type", "radio")
          .attr("value", option)
          .attr("id", selectID + "-button")
          .attr("name", "toggle")
          .attr("class", "form-check-input");

        // Add the text label
        inputRow
          .append("label")
          .text(layerOptions[option].name)
          .attr("for", selectID + "-button")
          .attr("class", "form-check-label");

        // Add the circles for legend
        inputRow
          .append("div")
          .attr("class", "rounded-circle d-inline-block align-middle")
          .style("margin-left", "5px")
          .style("width", RADIUS * 3 + "px")
          .style("height", RADIUS * 3 + "px")
          .style("background-color", layerOptions[option].color);
      }

      // Default selection
      layerSelect.select("input[value='single']").property("checked", true);

      // Make legend visible
      layerSelect.style("visibility", "visible");

      // Add the different annotations
      addScaleAnnotation();

      // Create and add circles for chosen major
      createPoints(this.course_coi_data, "chosen");
      // Create and add circles for other majors
      createPoints(this.curric_coi_data, "avg");

      // Populate the title with course title and score
      d3.select("#score")
        .text(chosenCourse.score)
        .attr(
          "title",
          chosenCourse.name + " has a COI score of " + chosenCourse.score
        );

      // Add an event listener to the radio buttons
      d3.selectAll("input[name='toggle']").on("change", function () {
        // Get the layer the user selected
        var selectedLayer = d3.select(this).property("value");

        // Select the previously chosen layer
        var prev = d3.selectAll(".shown, " + courseId);

        // Variable to keep the currently selected layer
        var selected;

        // Check which layer is chosen
        if (selectedLayer == "single") {
          if (d3.select(".shown").attr("class").includes("chosen")) {
            selected = d3.select(courseId + ".chosen");
          } else {
            selected = d3.select(courseId + ".avg");
          }

          // Screen reader text for the specific course
          d3.select("#sr-text").text(
            `${chosenCourse.name} has a score of ${chosenCourse.score}.`
          );
        } else if (selectedLayer == "chosen") {
          // Screen reader text for the chosen major
          d3.select("#sr-text").text(
            `${chosenCourse.name} has a score of ${chosenCourse.score} compared to the major average of ${chosenCourse.score}.`
          );

          // If the user selected the major courses layer
          selected = d3.selectAll(".chosen");
        } else {
          // Screen reader text for layer with average scores
          d3.select("#sr-text").text(
            `${chosenMajor.name} has a score of ${chosenMajor.score} compared to the average of around 0.`
          );

          // If the user selected the major averages layer
          selected = d3.selectAll(".avg");
        }

        // Switch the layers
        switchLayers(prev, selected);
      });

      // Allow for the hiding and showing of different layers
      function switchLayers(hide, show) {
        // Hiding the previous layer
        // First transition: move circle(s) to the center of y axis
        hide
          .each(function (d) {
            if (d.name == vue.course_id) {
              d3.select(this).raise();
            }
          })
          .transition("moveout-vcenter")
          .duration(1000)
          .delay(function (d, i) {
            return i / 3;
          })
          .attr("cy", yCenter)
          .end()
          .then(() => {
            // Second transition: move circle(s) to the center of x axis
            hide
              .transition("moveout-hcenter")
              .duration(500)
              .delay(function (d, i) {
                return i / 3;
              })
              .attr("cx", x(0))
              .style("opacity", 0)
              .end()
              .then(() => {
                hide.style("visibility", "hidden");
                show.style("visibility", "visible");
                hide.classed("shown", false);
                show.classed("shown", true);

                // Layer to show
                // Third transition: move circle(s) to their respective x positions
                show
                  .each(function (d) {
                    if (d.name == vue.course_id) {
                      d3.select(this).raise();
                    }
                  })
                  .transition("movein-vpoints")
                  .duration(1000)
                  .delay(function (d, i) {
                    return i / 3;
                  })
                  .style("opacity", 1)
                  .attr("cx", function (d) {
                    return d.x;
                  })
                  .end()
                  .then(() => {
                    // Fourth transition: move circle(s) to their respective y positions
                    show
                      .transition("movein-hpoints")
                      .duration(500)
                      .delay(function (d, i) {
                        return i / 3;
                      })
                      .attr("cy", function (d) {
                        if (show._groups[0].length == 1) {
                          return yCenter;
                        } else {
                          return d.y;
                        }
                      })
                      .end();
                  });
              });
          });
      }

      // Function to generate and hide all the points onto the svg
      function createPoints(data, layer) {
        var labelName;
        if (layer == "chosen") {
          labelName = "course_id";
        } else {
          labelName = "curric_name";
        }

        // Filter out data and create a new array to feed into force simulation
        var nodes = data
          .filter(function (node) {
            if (
              node.score == null ||
              node[labelName].includes("MASTERS") ||
              node[labelName].startsWith("MS") ||
              node[labelName].trim() == "GRADUATE SCHOOL" ||
              node[labelName].trim() == "UW ACADEMY"
            ) {
              return false;
            } else {
              return true;
            }
          })
          .map(function (node) {
            var score = node.score;

            return {
              x: x(score), // Scale the score from -5 to 5
              y: yCenter, // Set the default height of the point
              score: Math.round(score * 100) / 100, // Round the score to two decimal places
              name: node[labelName], // Give the course/major its name
              major: "curric" in node ? node.curric : majorPicked, // Major codes to each point
            };
          });

        // Add chosen course to the major averages layer
        if (layer != "chosen") {
          nodes.push({
            x: chosenCourse.x,
            y: chosenCourse.y,
            score: chosenCourse.score,
            name: chosenCourse.name,
            major: chosenCourse.major,
          });
        }

        // Specify force specifications for the circles
        var force = d3
          .forceSimulation(nodes)
          .force("forceX", d3.forceX((d) => d.x).strength(1)) // Force points to their respective x position
          .force("forceY", d3.forceY(yCenter).strength(0.1)) // Push points towards the center of the svg
          .force(
            "charge",
            d3.forceManyBody().distanceMax(3).distanceMin(2).strength(1) // Set minimum and maximum distance between all of the points
          )
          .force(
            "collide",
            d3
              .forceCollide()
              .radius(RADIUS * 1.1)
              .strength(1)
          ) // Specify the seperation of points
          .on("tick", tick)
          .stop();

        function tick() {
          for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            node.cx = node.x;
            node.cy = node.y;
          }
        }

        // Run force simulation n times
        const NUM_ITERATIONS = 200;
        force.tick(NUM_ITERATIONS);
        force.stop();

        // Add the points to the plot
        // Depending on whether the course is chosen, the fill color and opacity will be different
        svg
          .selectAll("." + layer + " circle") // Select current layer
          .data(nodes) // Input data
          .enter()
          .append("circle")
          .style("visibility", function (d) {
            // Hide point if not picked
            if (d.name == vue.course_id) {
              return "visible";
            } else {
              return "hidden";
            }
          })
          .attr("fill", function (d) {
            if (d.major == majorPicked && layer == "avg") {
              chosenMajor = d; // Keep track of chosen major
            }
            // Color circles by cateogry
            if (d.name == vue.course_id) {
              chosenCourse = d; // Keep track of chosen course
              return courseColor;
            } else if (layer == "chosen") {
              return majorColor;
            } else {
              return avgColor;
            }
          })
          .attr("opacity", function (d) {
            if (d.name == vue.course_id && layer == "chosen") {
              return 1; // Show the chosen course
            } else {
              return 0; // Hide everything else
            }
          })
          .attr("stroke", function (d) {
            if (d.name == vue.course_id) {
              return "black";
            } else {
              return "none";
            }
          })
          .attr("cx", function (d) {
            if (d.name == vue.course_id && layer == "chosen") {
              return d.x; // Set horizontal position of the chosen course
            } else {
              return x(0); // Set the default point of all other points
            }
          })
          .attr("cy", function () {
            return yCenter; // Start off in the middle of the svg
          })
          .attr("class", function (d) {
            var fullClass = "";
            if (d.name == vue.course_id) {
              fullClass += "shown ";
            }

            if (layer == "chosen") {
              fullClass += "chosen"; // Set class of the circle
            } else {
              fullClass += "avg"; // Set class of the circle
            }

            return fullClass;
          })
          .attr("id", function (d) {
            return d.name.replace(/\s/g, "_"); // Set id for each course
          })
          .attr("score", function (d) {
            return d.score; // Keep track of score for each course -- not sure this is needed
          })
          .attr("r", function (d) {
            if (d.name == vue.course_id) {
              return RADIUS * 1.5;
            } else {
              return RADIUS;
            }
          })
          .each(function () {
            // Enable mouse over interaction
            d3.select(this)
              .on("mouseover", function (event, d) {
                // Change point properties when hovered over
                d3.select(this)
                  .raise()
                  .transition()
                  .duration(50)
                  .style("stroke", "black")
                  .attr("r", d3.select(this).attr("r") * 1.2);

                // Make the tooltip visible when point is hovered
                tooltip
                  .style("opacity", 1)
                  .style("visibility", "visible")
                  .html(
                    "<i>" +
                      d.name +
                      "</i><br>" +
                      "COI: <strong>" +
                      d.score +
                      "</strong>"
                  );
              })
              .on("mousemove", function (event) {
                // Move the tooltip as the user moves the pointer
                tooltip
                  .style("left", event.pageX + 5 + "px")
                  .style("top", event.pageY - 50 + "px");
              })
              .on("mouseout", function () {
                // Return point to default properties
                d3.select(this)
                  .transition()
                  .duration(50)
                  .style("stroke", function (d) {
                    if (d.name == vue.course_id) {
                      return "black";
                    } else {
                      return "none";
                    }
                  })
                  .attr("r", function (d) {
                    if (d.name == vue.course_id) {
                      return RADIUS * 1.5;
                    } else {
                      return RADIUS;
                    }
                  });

                d3.select(courseId).raise();

                // Hide the tooltip
                tooltip.style("opacity", 0).style("visibility", "visible");
              });
          });
      }

      // Add text annotation
      function addScaleAnnotation() {
        var labelPosY = height / 1.3;
        var sublabelPosY = height / 1.15;
        var mainSize = "65%";
        var subSize = "95%";

        svg
          .append("text")
          .attr("class", "coi-labels fw-bold")
          .style("font-size", mainSize)
          //.style("font-weight", "bold")
          .attr("x", x(3.31))
          .attr("y", labelPosY)
          .attr("text-anchor", "right")
          .html("positive outcomes")
          .append("tspan")
          .style("font-weight", "normal")
          .style("font-size", subSize)
          .attr("x", x(1.45))
          .attr("y", sublabelPosY)
          .attr("text-anchor", "right")
          .html("more students earned credit than predicted");

        svg
          .append("text")
          .style("font-size", mainSize)
          .style("font-weight", "bold")
          .attr("x", x(-5))
          .attr("y", labelPosY)
          .attr("text-anchor", "left")
          .html("negative outcomes")
          .append("tspan")
          .style("font-weight", "normal")
          .style("font-size", subSize)
          .attr("x", x(-5))
          .attr("y", sublabelPosY)
          .attr("text-anchor", "left")
          .html("fewer students earned credit than predicted");
      }
    },
    getCourseCOI() {
      let url = "/api/v1/coi/course/" + this.course.department_abbrev,
        vue = this;
      this.axios
        .get(url)
        .then((response) => {
          vue.course_coi_data = response.data;
          this.getData();
        })
        .catch(function (error) {
          vue.course_coi_data = {};
        });
    },
    getCurricCOI() {
      let vue = this;
      this.axios
        .get("/api/v1/coi/curric/")
        .then((response) => {
          vue.curric_coi_data = response.data;
          this.generateRect();
        })
        .catch(function (error) {
          vue.curric_coi_data = {};
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css2?family=Open+Sans&display=swap");

text {
  font-family: "Open Sans", sans-serif;
}

#scatter svg {
  margin-right: auto;
  margin-left: auto;
}

.tooltip {
  width: auto;
}

.axis text {
  fill: black;
}

.axis line,
.axis path {
  stroke: gray;
  stroke-width: 1px;
}

.grid {
  stroke: grey;
}

#more {
  font-style: italic;
  fill: green;
}

#less {
  font-style: italic;
  fill: red;
}

#layer-select {
  font-size: 100%;
  visibility: hidden;
  padding: 1% 2%;
  margin: 1rem;
}

#score {
  font-size: 200%;
  font-weight: bold;
}

.coi-score {
  padding: 1% 2%;
  margin: 1rem;
}

#upper {
  margin-top: 1rem;
}

#coiGraph path.domain,
#coiGraph g.tick {
  stroke-width: 1px;
}

#coiGraph g.tick line {
  stroke-width: 1px;
}

.screen-reader-only {
  position: absolute;
  height: 1px;
  width: 1px;
  clip: rect(1px 1px 1px 1px); // IE 6 and 7
  clip: rect(1px, 1px, 1px, 1px);
  clip-path: polygon(0px 0px, 0px 0px, 0px 0px);
  -webkit-clip-path: polygon(0px 0px, 0px 0px, 0px 0px);
  overflow: hidden !important;
}

#coi-tooltip {
  width: auto;
}

.carousel-caption {
  position: initial;
  right: 15%;
  bottom: 1.25rem;
  left: 15%;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
  color: #000;
}

.carousel-indicators [data-bs-target] {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.shown {
  visibility: visible;
  pointer-events: all;
}
</style>
