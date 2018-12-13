<template>
  <div>
    <div class="navbar">
      <div class="login-disp">
        <div v-if="username != null">
          {{username}}
        </div>
        <div v-else>
          ログインしていません <button v-on:click="loginModal=true">(login)</button>
        </div>
      </div>
    </div>
    <div class="modal-mask" v-if="loginModal===true">
      <div class="modal-wrapper">
        <div class="dialog-login">
          <p>username:<input type="text" v-model="username"> </p>
          <p>password:<input type="password" v-model="password"></p>
          <p> <button v-on:click="login(username,password)">submit</button> </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import axios from "axios";
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default {
  data: vm => ({
    username: null,
    password: null,
    loginModal: false
  }),
  created() {
    this.state();
  },
  methods: {
    get_host() {
      var h = location.host;
      if (location.port == 8080) {
        h = location.hostname + ":8000";
      }
      return h;
    },
    async state() {
      var host = this.get_host();
      var response = await axios.get("http://" + host + "/jong/account");
      console.log(response);
      this.username = response.data.username;
    },
    async login(u, p) {
      var host = this.get_host();
      var response = await axios.post("http://" + host + "/jong/login", {
        username: u,
        password: p
      },{
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      });
      this.state();
    },
    async logout() {
      var host = this.get_host();
      var response = await axios.post("http://" + host + "/jong/logout");
    }
  }
};
</script>
<style scoped>
.navbar {
  width: 100%;
  height: 40px;
  background-color: gray;
  margin: 0px;
  color: white;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
.login-disp {
  text-align: right;
}
.dialog-login {
  position: relative;
  background-color: lightgray;
  width: 600px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}
.selection {
  min-width: 200px;
}

.dialog-body {
  margin-top: 20px;
}
.dialog-footer {
  margin-top: 50px;
}
.dialog-exit {
  position: absolute;
  top: 5px;
  right: 5px;
}
</style>