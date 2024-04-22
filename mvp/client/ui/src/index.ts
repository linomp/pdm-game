import './global.css'
import { initErrorHandlers } from './errorHandlers'
import App from './App.svelte'
import { OpenAPI } from './api/generated'

(async function () {
  initErrorHandlers()
  document.body.innerHTML = ''
  OpenAPI.BASE = import.meta.env.VITE_API_BASE;
  new App({ target: document.body })
}())
