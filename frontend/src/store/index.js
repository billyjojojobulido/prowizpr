import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)

//The store modules need to be successfully refactored into the folder
const store = new Vuex.Store({
    state: {
        authenticated: false,
        is_admin: false,
        uid: 0,
    },

    plugins:[
      createPersistedState({
          storage: window.localStorage
      })
    ],

    // getters
    getters: {
        checkAuthenticated: (state) => {
            return state.authenticated;
        },
        getUID: (state) => {
            if (state.authenticated) {
                return state.uid;
            }
            return -1;
        },
        isAdmin: (state) =>{
            return state.is_admin
        }
    },

    // mutations
    mutations: {
        authenticate (state, uid) {
            state.authenticated = true;
            state.uid = uid;
        },
        admin_auth (state, is_admin){
            state.is_admin = is_admin;
        },
        logout (state){
            state.authenticated = false;
            state.username = null;
            state.is_admin = false;
            state.uid = 0;
        }
    }
})

export default store;
