<template>
  <div>
    <b-container class="headerCont" fluid>
      <div id="nav">
        <b-navbar class="navBar fixed-top" type="light">
          <b-navbar-nav>
            <b-nav-item nuxt-link to="/"> Home </b-nav-item>
            <b-nav-item nuxt-link to="/about"> About </b-nav-item>
            <b-nav-item nuxt-link to="/help"> Help </b-nav-item>
          </b-navbar-nav>
        </b-navbar>
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style scoped>
.navBar {
  background: #8fd19e;
}

#nav {
  color: #000000;
}

#nav a.router-link-exact-active {
  color: #21392e;
}

.headerCont {
  margin-bottom: 5vh;
}
</style>
