import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//The store modules need to be successfully refactored into the folder
const store = new Vuex.Store({
    state: {
        authenticated: false,
        uid: 0,
        username: null,
    },

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
        getUsername: (state) => {
            if (state.authenticated) {
                return state.username;
            }
            return null;
        }
    },

    // mutations
    mutations: {
        authenticate (state, username, uid) {
            state.authenticated = true;
            state.uid = uid;
            state.username = username;
        },
        logout (state){
            state.authenticated = false;
            state.username = null;
            state.uid = 0;
        }
    }
})

export default store;
