import { render } from '@testing-library/svelte'
import Chart from './TimeSeriesChart.svelte'
import '@testing-library/jest-dom/extend-expect'


describe('Chart', () => {
    it('renders', () => {
        render(Chart)
    })
})
