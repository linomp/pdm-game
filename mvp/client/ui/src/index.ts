import 'src/global.css'
import {initErrorHandlers} from 'src/errorHandlers'
import App from 'src/App.svelte'
import {OpenAPI} from 'src/shared/api'

(async function () {
    initErrorHandlers()
    document.body.innerHTML = ''
    OpenAPI.BASE = import.meta.env.VITE_API_BASE;
    new App({target: document.body})
}())
