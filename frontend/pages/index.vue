<template>
  <div>
    <h3 class="title">ClinicalTrailsEndpointExtraction</h3>
    <b-container class="container">
      <b-row class="projectForm">
        <b-col class="varCol">
          <h4>Filter - Settings</h4>
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
              <b-button variant="primary" @click="sendParams()">
                Submit
              </b-button>
            </b-form>
          </div>
        </b-col>
        <b-col />
        <b-col class="groupCol">
          <h4>Aggragation - Settings</h4>
          <b-form-group
            v-slot="{ ariaDescribedby }"
            label="Select following aggregation options:"
          >
            <b-form-checkbox-group
              id="groupbyCheckboxGroup"
              v-model="selected"
              :options="options"
              :aria-describedby="ariaDescribedby"
              name="flavour-1"
            ></b-form-checkbox-group>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <b-row>
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
        <b-col />
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
      change: '',
      variable: '',
      reference: '',
      condition: '',
      timepoint: '',
      selected: [],
      options: [
        { text: 'Change', value: 'change' },
        { text: 'Variable', value: 'variable' },
        { text: 'Condition', value: 'condition' },
        { text: 'reference', value: 'reference' },
      ],
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
  methods: {
    async sendParams() {
      const params = {
        Change: this.change,
        Variable: this.variable,
        Reference: this.reference,
        Condition: this.condition,
        Timepoint: this.timepoint,
      }
      try {
        const response = await this.$axios.post('/filter', params)
        this.items = response.data.map((JSON) => {
          return {
            ...JSON,
          }
        })
      } catch (e) {
        alert(e.toString())
      }
    },
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
  min-width: 40%;
}

.groupCol {
  min-width: 40%;
}

.outCol {
  min-width: 100%;
}
</style>
