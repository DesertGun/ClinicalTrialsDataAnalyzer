<template>
  <div>
    <h3 class="title">ClinicalTrailsEndpointExtraction</h3>
    <b-container class="container">
      <b-row class="projectForm">
        <b-col class="varCol">
          <h4>Test.1</h4>
          <div>
            <b-form class="forms">
              <b-form-group
                id="projectName"
                description="Name of a new project is required"
                label="Project name:"
                label-for="projectNameInput"
              >
                <b-form-input
                  id="projectNameInput"
                  v-model="projectName"
                  class="projectNameInput"
                  placeholder="Enter project Name"
                  required
                  type="text"
                />
              </b-form-group>

              <b-form-group
                id="projectDesc"
                description="Description is optional"
                label="Project description:"
                label-for="inputProjectDesc"
              >
                <b-form-input
                  id="inputProjectDesc"
                  v-model="projectDesc"
                  placeholder="Enter project-description"
                  type="text"
                />
              </b-form-group>
              <b-button variant="primary"> Submit </b-button>
            </b-form>
          </div>
        </b-col>
        <b-col />
        <b-col class="outCol">
          <h4>Test.2</h4>
          <div>
            <b-table striped hover :items="items"></b-table>
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
      items: [
        { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
        { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
        { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
        { age: 38, first_name: 'Jami', last_name: 'Carney' },
      ],
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
  min-width: 45%;
}

.outCol {
  min-width: 45%;
}
</style>
