<template>
  <div>
    <h3 class="title">ClinicalTrailsEndpointExtraction</h3>
    <b-container class="container">
      <b-row class="projectForm">
        <b-col class="varCol">
          <h4>Variable - Settings</h4>
          <div>
            <b-form class="forms">
              <b-form-group
                id="projectName"
                description="Enter the change type"
                label="Change:"
                label-for="changeInput"
              >
                <b-form-input
                  id="changeInput"
                  v-model="change"
                  class="changeInput"
                  placeholder="E.g., Count of Participants"
                  required
                  type="text"
                />
              </b-form-group>

              <b-form-group
                id="reference"
                description="Enter the reference"
                label="Reference:"
                label-for="referenceInput"
              >
                <b-form-input
                  id="referenceInput"
                  v-model="reference"
                  placeholder="E.g., Number of Participants Analyzed"
                  type="text"
                />
              </b-form-group>
              <b-form-group
                id="variable"
                description="Enter the Variable"
                label="Variable:"
                label-for="variableInput"
              >
                <b-form-input
                  id="variableInput"
                  v-model="variable"
                  placeholder="E.g., Abnormal Electrocardiogram (ECG) Interval"
                  type="text"
                />
              </b-form-group>
              <b-form-group
                id="timepoint"
                description="Enter the Timepoint"
                label="Timepoint:"
                label-for="timepointInput"
              >
                <b-form-input
                  id="timepointInput"
                  v-model="timepoint"
                  placeholder="E.g., Approximately 42 days"
                  type="text"
                />
              </b-form-group>
              <b-form-group
                id="condition"
                description="Enter the Condition"
                label="Condition:"
                label-for="conditionInput"
              >
                <b-form-input
                  id="conditionInput"
                  v-model="condition"
                  placeholder="E.g., Type 2 Diabetes"
                  type="text"
                />
              </b-form-group>
              <b-button variant="primary"> Submit </b-button>
            </b-form>
          </div>
        </b-col>
        <b-col />
        <b-col class="outCol">
          <h4>Results</h4>
          <div class="mb-2">
            <b-table
              sticky-header="500px"
              :no-border-collapse="noCollapse"
              responsive
              striped
              hover
              :items="items"
            ></b-table>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stickyHeader: true,
      noCollapse: false,
      items: [],
      change: null,
      variable: null,
      reference: null,
      condition: null,
      timepoint: null,
    }
  },
  async mounted() {
    try {
      const response = await this.$axios.get('/results')

      this.items = response.data.map((JSON) => {
        return {
          ...JSON,
        }
      })
    } catch (e) {
      alert(e.toString())
    }
  },
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 60vh;
  display: flex;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 200;
  font-size: 300%;
  color: #35495e;
  letter-spacing: 1px;
  text-align: center;
}

.projectForm {
  justify-content: center;
  min-width: 100%;
}

.varCol {
  min-width: 50%;
}

.outCol {
  min-width: 80%;
}
</style>
