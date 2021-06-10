<template>
  <div>
    <h3 class="title">ClinicalTrailsEndpointExtraction</h3>
    <b-container class="container">
      <b-row class="projectForm">
        <b-col class="varCol">
          <h4>Filter - Settings</h4>
          <div>
            <p>Enter the change type:</p>
            <div class="p-auto">
              <vue-typeahead-bootstrap
                id="changeInput"
                v-model="change"
                class="changeInput"
                placeholder="E.g., Count of Participants"
                required
                :data="autocompleteChange"
                type="text"
              />
            </div>
            <p>Enter the reference:</p>
            <div class="p-auto">
              <vue-typeahead-bootstrap
                id="referenceInput"
                v-model="reference"
                placeholder="E.g., Number of Participants Analyzed"
                :data="autocompleteReference"
                type="text"
              />
            </div>
            <p>Enter the Variable:</p>
            <div class="p-auto">
              <vue-typeahead-bootstrap
                id="variableInput"
                v-model="variable"
                placeholder="E.g., Abnormal Electrocardiogram (ECG) Interval"
                type="text"
                :data="autocompleteVariable"
              />
            </div>
            <p>Enter the Timepoint:</p>
            <div class="p-auto">
              <vue-typeahead-bootstrap
                id="timepointInput"
                v-model="timepoint"
                placeholder="E.g., Approximately 42 days"
                type="text"
                :data="autocompleteTimepoint"
              />
            </div>
            <p>Enter the Condition:</p>
            <div class="p-auto">
              <vue-typeahead-bootstrap
                id="conditionInput"
                v-model="condition"
                placeholder="E.g., Type 2 Diabetes"
                type="text"
                :data="autocompleteCondition"
              />
            </div>
            <b-button variant="primary" @click="sendParams()">
              Submit
            </b-button>
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
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap'

export default {
  components: {
    VueTypeaheadBootstrap,
  },
  data() {
    return {
      stickyHeader: true,
      noCollapse: false,
      items: [],
      autocompleteItems: [],
      autocompleteChange: [],
      autocompleteReference: [],
      autocompleteVariable: [],
      autocompleteTimepoint: [],
      change: '',
      variable: '',
      reference: '',
      condition: '',
      timepoint: '',
      selected: [],
      options: [
        { text: 'Change', value: 'Change' },
        { text: 'Variable', value: 'Variable' },
        { text: 'Condition', value: 'Condition' },
        { text: 'reference', value: 'Reference' },
      ],
    }
  },
  async mounted() {
    try {
      this.items = await this.$axios
        .get('/results')
        .then((response) => response.data)
      this.autocompleteItems = this.items
      this.autocompleteChange = this.autocompleteItems.map((d) => d.Change)
      this.autocompleteChange = Array.from(new Set(this.autocompleteChange))
      this.autocompleteReference = this.autocompleteItems.map(
        (d) => d.Reference
      )
      this.autocompleteReference = Array.from(
        new Set(this.autocompleteReference)
      )
      this.autocompleteVariable = this.autocompleteItems.map((d) => d.Variable)
      this.autocompleteVariable = Array.from(new Set(this.autocompleteVariable))
      this.autocompleteTimepoint = this.autocompleteItems.map(
        (d) => d.Timepoint
      )
      this.autocompleteTimepoint = Array.from(
        new Set(this.autocompleteTimepoint)
      )
      this.autocompleteCondition = this.autocompleteItems.map(
        (d) => d.Condition
      )
      this.autocompleteCondition = Array.from(
        new Set(this.autocompleteCondition)
      )
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
        GroupByOptions: this.selected,
      }
      try {
        this.items = await this.$axios
          .post('/filter', params)
          .then((response) => response.data)
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
