import './shared/ArrayExtensions'

global.fetch = window.fetch = () => new Promise(() => { })
global.scrollTo = window.scrollTo = () => { }

afterEach(() => {
  vi.restoreAllMocks()
})
